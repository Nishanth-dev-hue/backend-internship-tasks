data = {
    "class_intervals": ["0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70"],
    "frequencies": [12, 6, 8, 23, 32, 19, 10]
}
for i in range(1, len(data["frequencies"]) - 1):
    if data["frequencies"][i] > data["frequencies"][i-1] and data["frequencies"][i] > data["frequencies"][i+1]:
        print("Mode :",
            int(data["class_intervals"][i].split("-")[0])
            +
            (
                (data["frequencies"][i] - data["frequencies"][i-1])
                /
                (
                    2*data["frequencies"][i]
                    - data["frequencies"][i-1]
                    - data["frequencies"][i+1]
                )
            )
            *
            (
                int(data["class_intervals"][i].split("-")[1])
                - int(data["class_intervals"][i].split("-")[0])
            )
        )
        break
