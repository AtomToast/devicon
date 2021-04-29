import re
from pathlib import Path


class SvgIdUpdater:
    # look for anything that is between ` id="` and `"`
    id_declare_pattern = r"(?<= id=(\"|')).+?(?=(\"|'))"

    # look for anything that is between `"url(#` and `)"`
    id_use_pattern = r"(?<=\"url\(#).+?(?=\)\")"

    # pattern made up of both
    id_pattern = f"{id_declare_pattern}|{id_use_pattern}"

    def __init__(self):
        self.id_generator = None
        self.old_to_new_ids_dict = None


    def update_id(self, filepath: Path):
        """
        Update the ids inside an svg file.
        """
        # reset the data for each file
        self.reset(filepath.stem)

        # can switch to other patterns if needed
        search_regexp = re.compile(SvgIdUpdater.id_pattern)
            
        with open(filepath, "r+") as file:
            print("Opening " + file.name)

            new_content = search_regexp.sub(self.sub_id, file.read())

            # write to a new file
            new_path = filepath.with_name(filepath.stem + "-written" + filepath.suffix)
            with open(new_path, "w") as new_file:
                new_file.write(new_content)
                print("Finished substituting. Writing to " + new_file.name)
                
            # overwrite same file
            # file.write(new_content)  # overwrite


    def reset(self, filename: str):
        self.id_generator = self.id_generator_setup(filename)
        self.old_to_new_ids_dict = {}


    def id_generator_setup(self, filename: str):
        num = 0
        while True:
            yield f"{filename}-{num}"
            num += 1


    def sub_id(self, match):
        old = match.group()
        try:
            # see if we already have an id for this
            new = self.old_to_new_ids_dict[old]
        except KeyError:
            # if not, make one
            new = next(self.id_generator)
            self.old_to_new_ids_dict[old] = new
        finally:
            print("Old Id:", old, ". New Id:", new)
            return new
