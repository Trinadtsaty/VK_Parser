from slicers import apply_slicer, get_name, add_intersection_and_any


inp = 'people_open_with_groups.json'

groups_to_check_in = ['Fantasy Premier League', 'Omar Momani']

result = apply_slicer(inp, groups_to_check_in, output_path="people_123.json")

print(result)