data = [{"name": "others", "units": 0}]
total_bill = 0
unit_sum = 0
per_unit_bill = 0
entry_count = 0

if __name__ == "__main__":

    total_bill = float(input(" Enter Total Bill: "))

    while True:
        name = input("👤 Name: ").lower()

        other = abs(float(input(" Other Units (shared or unaccounted): ")))
        data[0]["units"] += other
        unit_sum += other

        starting_unit = abs(float(input(" Starting Units: ")))
        ending_unit = abs(float(input(" Ending Units: ")))

        if starting_unit > ending_unit:
            print(" Starting units must be smaller than ending units")
            break

        total_units = ending_unit - starting_unit
        unit_sum += total_units
        entry_count += 1

        found = False
        for person in data:
            if person["name"] == name:
                person["units"] += total_units
                print(f" Entry {entry_count}: {name} updated by {total_units} units.")
                found = True
                break

        if not found:
            data.append({"name": name, "units": total_units})
            print(f" Entry {entry_count}: {name} created with {total_units} units.")

        # Bill Calculation
        per_unit_bill = total_bill / unit_sum
        print("\n📊 Final Summary")
        print(f"Total Bill        : {round(total_bill, 2)}")
        print(f"Total Units ⚡     : {round(unit_sum, 2)}")
        print(f"Per Unit Cost     : {round(per_unit_bill, 2)}\n")

        for person in data:
            bill_amount = round(per_unit_bill * person["units"], 2)
            print(f"{person['name'].capitalize():<10} → Units: {person['units']:.2f}, Bill: Rs. {bill_amount:.2f}")

        stop = input(" Do you want to add more? (yes/no): ").lower()
        if stop == "no":
            break



    # 🧾 Final Summary

