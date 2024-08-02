import os
import re
import yaml

def GDConvertorToGP (directory):
    # folder where the files are converted to

    os.mkdir('./ClaimData')
    allfiles = os.listdir(directory)
    for count, filename in enumerate(sorted(os.listdir(directory))):
        path = directory + filename
        with open(path, "r") as file:
            content = file.read()

        newFilePath = os.path.join("ClaimData/",f"{count}.yml")

        owner_uuid_match = re.search(re.compile(r'owner-uuid="([^"]*)"'), content)
        lesser_boundary_match = re.search(re.compile(r'lesser-boundary-corner="([^"]*)"'), content)
        greater_boundary_match = re.search(re.compile(r'greater-boundary-corner="([^"]*)"'), content)

        default_owner_uuid = ""
        default_lesser_boundary = "1;-56;-20"
        default_greater_boundary = "9;-54;-1"

        owner_uuid = owner_uuid_match.group(1) if owner_uuid_match else default_owner_uuid
        lesser_boundary = lesser_boundary_match.group(1) if lesser_boundary_match else default_lesser_boundary
        greater_boundary = greater_boundary_match.group(1) if greater_boundary_match else default_greater_boundary
        
        lesser_boundary_parts = lesser_boundary.split(';')
        greater_boundary_parts = greater_boundary.split(';')

        if len(lesser_boundary_parts) != 3:
            lesser_boundary = default_lesser_boundary
        if len(greater_boundary_parts) != 3:
            greater_boundary = default_greater_boundary
        data = {
            'Lesser Boundary Corner': f'land;{lesser_boundary}',
            'Greater Boundary Corner': f'land;{greater_boundary}',
            'Owner': owner_uuid,
            'Builders': [],
            'Containers': [],
            'Accessors': [],
            'Managers': [],
            'Parent Claim ID': -1,
            'inheritNothing': False
        }
        with open(newFilePath, 'w') as new_file:
            yaml.dump(data, new_file, default_flow_style=False, sort_keys=False)

        print(f"Converted {filename}, created {count}.yml  :>")

# GriefDefender dir example = './test/'

GDConvertorToGP('./test/')
