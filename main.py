import logging
from logging.config import fileConfig
from typing import TextIO, Union

fileConfig("log.ini")

logger = logging.getLogger("dev")


def get_input_data(file_name: str) -> tuple[dict[int, Union[list[list[int]], str]], list[str]]:
    f: TextIO = open(file_name)

    rules: dict[int, Union[list[list[int]], str]] = {}

    next_line = f.readline().strip()
    while next_line != "":
        index, body = next_line.split(":")
        if body.strip() == '"a"' or body.strip() == '"b"':
            rules[int(index)] = body.strip().replace("\"", "")
        else:
            body = body.split("|")
            rules[int(index)] = [list(map(lambda s: int(s), b.strip().split(" "))) for b in body]
        next_line = f.readline().strip()

    messages: list[str] = []
    next_line = f.readline().strip()
    while next_line != "":
        messages.append(next_line)
        next_line = f.readline().strip()

    return rules, messages


def alt_prod(*args):
    pools = [tuple(pool) for pool in args]
    result = [[]]
    for pool in pools:
        result = [x + y for x in result for y in pool]
    return result


def compile_recursion(rules: dict[int, Union[list[list[int]], str]],
                      num: int,
                      mem: dict[int, Union[list[list[int]], list[list[str]]]],
                      ) -> Union[list[list[int]], list[list[str]]]:
    if num in mem:
        return mem[num]
    if rules[num] == "a" or rules[num] == "b":
        mem[num] = [[rules[num]]]
        return [[rules[num]]]
    result: list[list[int]] = []
    for l in rules[num]:
        pro = [compile_recursion(rules, n, mem) for n in l]
        p = list(alt_prod(*pro))
        result.extend(p)
    mem[num] = result
    return result


def message_valid_part_1(m: str, comps: dict[int, tuple[str, ...]]) -> bool:
    if len(m) != 24:
        return False
    if not m.startswith(comps[42]):
        return False
    if not m.startswith(comps[42], 8):
        return False
    if not m.startswith(comps[31], 16):
        return False
    return True


def message_valid_part_2(m: str, comps: dict[int, tuple[str, ...]]) -> bool:
    count_31 = 0
    count_42 = 0
    if len(m) % 8 != 0:
        return False
    if not m.startswith(comps[42]):
        return False
    if not m.startswith(comps[42], 8):
        return False
    i = 16
    while m.startswith(comps[42], i) and i < len(m) - 8:
        count_42 += 1
        i += 8
    while m.startswith(comps[31], i) and i < len(m) - 8:
        count_31 += 1
        i += 8
    if count_31 > count_42:
        return False
    if i != len(m) - 8:
        return False
    if not m.startswith(comps[31], i):
        return False
    return True


def solution_common(file_name: str) -> tuple[list[str], dict[int, tuple[str, ...]]]:
    rules, messages = get_input_data(file_name)
    logger.debug(rules)
    comp_42 = tuple("".join(map(str, r)) for r in compile_recursion(rules, 42, {}))
    comp_31 = tuple("".join(map(str, r)) for r in compile_recursion(rules, 31, {}))
    logger.debug(len(comp_31))
    logger.debug(list(map(len, comp_31)))
    logger.debug(len(comp_42))
    logger.debug(list(map(len, comp_42)))
    comps = {42: comp_42, 31: comp_31}
    logger.debug(list(map(len, messages)))
    return messages, comps


def solution_part_1(file_name: str) -> int:
    messages, comps = solution_common(file_name)
    count: int = 0
    for m in messages:
        count += int(message_valid_part_1(m, comps))
    return count


def solution_part_2(file_name: str) -> int:
    messages, comps = solution_common(file_name)
    count: int = 0
    for m in messages:
        if message_valid_part_2(m, comps):
            count += 1
    return count


if __name__ == '__main__':
    # logger.info(solution_part_1("inputData.txt"))
    logger.info(solution_part_2("inputData.txt"))
