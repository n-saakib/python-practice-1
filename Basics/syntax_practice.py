def safe_div(a: float, b: float) -> float:
    if b == 0:
        return None
    return round(a / b, 3)


def slugify(s: str) -> str:
    lower_s: str = s.lower().strip()

    cleaned_strs: list[str] = []
    string: str = ""

    # cleans punctuations
    for char in lower_s:
        if char.isalpha() or char.isdigit() or char == "-":
            string = string + char
        elif char.isspace():
            # If empty string, no need to add to the list
            if len(string) > 0:
                cleaned_strs.append(string)
            string = ""

    # Add the last word to the list
    if len(string) > 0:
        cleaned_strs.append(string)

    return "-".join(cleaned_strs)


def median(nums: list[float]) -> float:
    if len(nums) == 0:
        raise ValueError("The list is Empty")

    nums.sort()
    l: int = len(nums)

    if l % 2 == 1:
        return nums[l // 2]
    else:
        sum = nums[l // 2] + nums[(l // 2) - 1]
        return sum / 2.0
