#!/usr/bin/env python3
"""
간단한 추첨(당첨자 뽑기) 스크립트
사용법 예시:
  python raffle.py --participants "철수,영희,민수,수지,지우" --winners 2
  python raffle.py --file names.txt --winners 3

- `--participants` : 쉼표로 구분된 참가자 이름 목록
- `--file`         : 파일 경로 (한 줄에 한 이름)
- `--winners`      : 뽑을 당첨자 수 (기본값 1)

결과는 표준 출력으로 보여줍니다.
"""

import argparse
import random
import sys


def pick_winners(participants, k):
    """리스트 `participants`에서 무작위로 `k`명을 반환합니다.
    참가자 수보다 많은 수를 뽑으려 하면 ValueError를 발생시킵니다.
    """
    if k <= 0:
        raise ValueError("뽑을 인원수는 1 이상이어야 합니다.")
    if k > len(participants):
        raise ValueError("참가자 수보다 많은 당첨자를 뽑을 수 없습니다.")
    return random.sample(participants, k)


def read_participants_from_file(path):
    names = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            name = line.strip()
            if name:
                names.append(name)
    return names


def main():
    parser = argparse.ArgumentParser(description='랜덤 당첨자 추첨기')
    parser.add_argument('--participants', type=str, help='쉼표로 구분된 참가자 이름들')
    parser.add_argument('--file', type=str, help='참가자 이름이 들어있는 파일 (한 줄에 한 이름)')
    parser.add_argument('--winners', type=int, default=1, help='뽑을 당첨자 수 (기본 1)')

    args = parser.parse_args()

    participants = []

    if args.file:
        try:
            participants = read_participants_from_file(args.file)
        except Exception as e:
            print(f"파일을 읽는 중 오류 발생: {e}")
            sys.exit(1)
    elif args.participants:
        participants = [p.strip() for p in args.participants.split(',') if p.strip()]
    else:
        # 입력이 없으면 사용자에게 입력을 요청합니다.
        try:
            raw = input('참ㄱ가자 이름을 쉼표로 구분하여 입력하세요: ')
        except EOFError:
            print('입력이 필요합니다. --participants 또는 --file을 사용하거나 표준 입력으로 이름을 제공하세요.')
            sys.exit(1)
        participants = [p.strip() for p in raw.split(',') if p.strip()]

    if not participants:
        print('참가자 목록이 비어있습니다. 참가자를 확인하세요.')
        sys.exit(1)

    try:
        winners = pick_winners(participants, args.winners)
    except ValueError as e:
        print('오류:', e)
        sys.exit(1)

    print('\n=== 당첨자 발표 ===')
    for i, w in enumerate(winners, 1):
        print(f'{i}. {w}')


if __name__ == '__main__':
    main()
