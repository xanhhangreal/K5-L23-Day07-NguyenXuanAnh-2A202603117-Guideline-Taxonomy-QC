"""Chia ảnh cho các thành viên: mỗi ảnh được K người gán ĐỘC LẬP, tải cân bằng.

Ví dụ:
    python scripts/split_assign.py --members 123,456,789
    python scripts/split_assign.py --members 123,456,789,111,222 --copy-images   # nhóm 5 người -> K=3 tự động

Cùng danh sách mã thành viên + cùng --seed => cùng kết quả (bất kể thứ tự gõ), nên cả nhóm chạy ra giống nhau.
"""
from __future__ import annotations

import argparse
import random
import shutil
import stat
import sys
from collections import Counter

from common import IMAGES_DIR, MEMBER_RE, ROOT, QC_DIR, WORK_DIR, die, list_images, rel, write_csv


def is_redirected(path) -> bool:
    """Reject symlinks and Windows reparse points (including junctions)."""
    if path.is_symlink():
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--members", required=True, help="Danh sách mã thành viên, ngăn cách bằng dấu phẩy. VD: 123,456,789")
    ap.add_argument("--overlap", type=int, default=None,
                    help="Số người gán mỗi ảnh (K). Mặc định 2; nhóm đúng 5 người thì mặc định 3.")
    ap.add_argument("--seed", type=int, default=42, help="Seed ngẫu nhiên (mặc định 42; cả nhóm dùng chung).")
    ap.add_argument("--copy-images", action="store_true",
                    help="Copy ảnh được giao vào work/<mã>/images/ để upload lên CVAT.")
    args = ap.parse_args()

    members = [m.strip() for m in args.members.split(",") if m.strip()]
    if not all(MEMBER_RE.fullmatch(member) for member in members):
        die("Mỗi mã thành viên gồm ba chữ số, ví dụ 101,102.")
    if len(set(members)) != len(members):
        die("Có mã thành viên bị trùng trong --members: " + str([m for m, c in Counter(members).items() if c > 1]))
    if len(members) < 2:
        die("Nhóm cần tối thiểu 2 thành viên (--members 123,456).")
    if len(members) > 5:
        die("Nhóm tối đa 5 thành viên.")
    members = sorted(members)

    k = args.overlap if args.overlap is not None else (3 if len(members) == 5 else 2)
    if args.overlap is None and len(members) == 5:
        print("Nhóm 5 người: mỗi ảnh được 3 người gán (--overlap 3).")
    if k < 2:
        die("--overlap phải >= 2 (mỗi ảnh ít nhất 2 người gán, nếu không không đo được IAA).")
    if k > len(members):
        die(f"--overlap={k} lớn hơn số thành viên ({len(members)}).")
    if len(members) == 5 and k < 3:
        die("Nhóm 5 người yêu cầu mỗi ảnh được gán bởi ít nhất 3 người (--overlap 3).")

    images = list_images()
    if not images:
        die(f"Không thấy ảnh trong {rel(IMAGES_DIR)}. Hãy lấy ảnh theo hướng dẫn trong README (tải/giải nén vào data/images/).")

    all_images = set(images)

    rng = random.Random(args.seed)
    load = {m: 0 for m in members}
    assign = {}
    for img in images:
        order = members[:]
        rng.shuffle(order)
        order.sort(key=lambda m: load[m])  # sort ổn định: ít việc nhất lên trước, hoà thì theo thứ tự ngẫu nhiên
        chosen = sorted(order[:k])
        for m in chosen:
            load[m] += 1
        assign[img] = chosen

    adir = QC_DIR / "assignments"
    destinations = [QC_DIR.parent, QC_DIR, adir, QC_DIR / "assignment.csv"]
    destinations.extend(adir / f"{member}.txt" for member in members)
    if args.copy_images:
        destinations.append(WORK_DIR)
        for member in members:
            member_dir = WORK_DIR / member
            photos = member_dir / "images"
            destinations.extend([member_dir, photos])
            destinations.extend(photos / image for image, codes in assign.items() if member in codes)
    for destination in destinations:
        if is_redirected(destination):
            die(f"Đường dẫn đầu ra không được là symlink hoặc reparse point: {rel(destination)}.")
    if args.copy_images:
        for member in members:
            photos = WORK_DIR / member / "images"
            if photos.is_dir() and any(
                is_redirected(photo) or not photo.is_file() or photo.name not in all_images
                for photo in photos.iterdir()
            ):
                die(f"{rel(photos)} chứa file ngoài danh mục ảnh. Dời chúng trước khi chia ảnh.")

    rows = [{"image": image, "annotators": "|".join(codes), "n_annotators": len(codes)}
            for image, codes in assign.items()]
    write_csv(QC_DIR / "assignment.csv", ["image", "annotators", "n_annotators"], rows)
    adir.mkdir(parents=True, exist_ok=True)
    for old in adir.glob("*.txt"):
        if MEMBER_RE.fullmatch(old.stem) and old.stem not in members:
            old.unlink()
    for member in members:
        mine = [image for image, codes in assign.items() if member in codes]
        (adir / f"{member}.txt").write_text("\n".join(mine) + "\n", encoding="utf8")
        if args.copy_images:
            dst = WORK_DIR / member / "images"
            dst.mkdir(parents=True, exist_ok=True)
            for old in dst.iterdir():
                if old.name not in mine:
                    old.unlink()
            for image in mine:
                shutil.copy2(IMAGES_DIR / image, dst / image)

    print(f"\nTổng {len(images)} ảnh, {len(members)} người, mỗi ảnh {k} người gán độc lập (seed={args.seed}).")
    print(f"{'mã thành viên':<12}{'số ảnh':>8}")
    for m in members:
        print(f"{m:<12}{load[m]:>8}")
    print(f"\nĐã ghi: {rel(QC_DIR / 'assignment.csv')} và {rel(adir)}/<mã>.txt")
    if args.copy_images:
        print(f"Đã copy ảnh của từng người vào {rel(WORK_DIR)}/<mã>/images/ -> upload thư mục này lên CVAT.")
    else:
        print("Mẹo: thêm --copy-images để tự copy ảnh của mình vào work/<mã>/images/ rồi upload lên CVAT.")
    print("\nQUAN TRỌNG: chỉ gán ảnh trong danh sách của MÌNH và KHÔNG xem nhãn của người khác trước khi nộp.")
    print("Commit file assignment.csv này để cả nhóm dùng chung một bản.")


if __name__ == "__main__":
    sys.exit(main())
