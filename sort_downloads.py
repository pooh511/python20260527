"""
Downloads 폴더 정리 스크립트
- 이미지: *.jpg, *.jpeg  -> images/
- 데이터: *.csv, *.xlsx -> data/
- 문서: *.txt, *.doc, *.pdf -> docs/
- 압축: *.zip -> archive/

사용법 예:
    python sort_downloads.py           # 실제로 파일 이동
    python sort_downloads.py --dry-run # 이동 예정 파일만 출력

다운로드 폴더는 C:/Users/student/Downloads 로 고정합니다.
"""

from pathlib import Path
import shutil
import argparse

DOWNLOADS = Path(r"C:\Users\student\Downloads")
FOLDERS = {
    'images': ['jpg', 'jpeg'],
    'data': ['csv', 'xlsx'],
    'docs': ['txt', 'doc', 'pdf'],
    'archive': ['zip'],
}

# 확장자에서 대상 폴더를 찾기 위한 역맵 생성
EXT_TO_FOLDER = {}
for folder, exts in FOLDERS.items():
    for e in exts:
        EXT_TO_FOLDER[e.lower()] = folder


def ensure_dir(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def unique_target(path: Path) -> Path:
    """같은 이름 파일이 이미 있으면 _1, _2 ...를 붙여서 유일한 경로 반환"""
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    i = 1
    while True:
        candidate = parent / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1


def should_move(file: Path):
    return file.is_file() and file.suffix


def organize(dry_run: bool = False):
    if not DOWNLOADS.exists():
        print(f"다운로드 폴더가 없습니다: {DOWNLOADS}")
        return

    moved = []
    skipped = []

    for item in DOWNLOADS.iterdir():
        if not item.is_file():
            continue
        ext = item.suffix.lower().lstrip('.')
        if not ext:
            skipped.append(item)
            continue
        folder_name = EXT_TO_FOLDER.get(ext)
        if not folder_name:
            skipped.append(item)
            continue

        dest_dir = DOWNLOADS / folder_name
        ensure_dir(dest_dir)
        target = dest_dir / item.name
        target = unique_target(target)

        if dry_run:
            moved.append((item, target))
        else:
            try:
                shutil.move(str(item), str(target))
                moved.append((item, target))
            except Exception as e:
                print(f"이동 실패: {item} -> {target} : {e}")

    # 결과 출력
    if dry_run:
        print("Dry run: 다음 파일들이 이동될 예정입니다:")
    else:
        print("이동 완료: 다음 파일들이 이동되었습니다:")

    for src, dst in moved:
        print(f"{src.name} -> {dst.relative_to(DOWNLOADS)}")

    if skipped:
        print("\n건너뛴 파일(대상 확장자 아님 또는 폴더):")
        for s in skipped:
            print(s.name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Downloads 폴더 정리기')
    parser.add_argument('--dry-run', action='store_true', help='실제로 이동하지 않고 어떤 파일이 이동될지 출력')
    args = parser.parse_args()

    organize(dry_run=args.dry_run)
