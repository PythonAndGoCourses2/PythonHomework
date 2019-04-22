from PythonHomework.final_task.pycalc.core.calculator import solve


def main():
    expression = str(input())
    print(solve(expression))


if __name__ == '__main__':
    main()
