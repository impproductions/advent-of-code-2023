def print_map(m, *highlight_conditions):
    xsize = max(x for x, _ in m) + 1
    ysize = max(y for _, y in m) + 1
    chart = ""
    for y in range(ysize):
        for x in range(xsize):
            c = m[(x, y)]
            for condition, replace in highlight_conditions:
                if condition((x, y)):
                    c = replace(m[(x, y)]) if callable(replace) else replace
            chart += c

        chart += "\n"

    print(chart)
