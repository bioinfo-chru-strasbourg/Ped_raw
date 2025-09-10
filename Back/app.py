from flask import Flask, jsonify, request, session, send_file, send_from_directory
from flask_cors import CORS
import json
import glob
import logging as log
from upload import (
    get_lines_content,
    check_extension,
    get_rows_list,
    get_columns,
    merge_peds,
    fill_dict,
    check_fam_id,
)
import os


def set_log_level(verbosity: str):
    verbosity = verbosity.lower()
    configs = {
        "debug": log.DEBUG,
        "info": log.INFO,
        "warning": log.WARNING,
        "error": log.ERROR,
        "critical": log.CRITICAL,
    }
    if verbosity not in configs.keys():
        raise ValueError(
            f"Unknown verbosity level: {verbosity}\nPlease use any in: {configs.keys()}"
        )
    log.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=configs[verbosity],
    )


set_log_level("debug")


# instantiate the app
app = Flask(__name__)
try:
    secret_key = os.environ["FLASK_SECRET_KEY"]
except KeyError:
    log.warning("No secret key found in environment, using default one.")
    secret_key = '_5#y2L"F4Q8z77ec]/'
app.secret_key = secret_key


# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


##PED


def get_files():
    path_to_data = "../Data/"
    files = glob.glob(path_to_data + "*.json")
    return files


def get_name_file(files: list, mode: str):
    if mode == "split":
        file_list = []
        for file in files:
            split = file.split("/")
            file_list.append(split[len(split) - 1][:-5])
        return file_list
    elif mode == "get":
        my_file = "../Data/" + files + ".json"
        return my_file


def ped_code(line):
    if line["sex"] == "M":
        line["sex"] = "1"
    elif line["sex"] == "F":
        line["sex"] = "2"
    else:
        line["sex"] = "0"
    if line["phenotype"] == "Unaffected":
        line["phenotype"] = "1"
    elif line["phenotype"] == "Affected":
        line["phenotype"] = "2"
    else:
        line["phenotype"] = "0"
    return line


@app.route("/files", methods=["GET", "POST"])
def all_files():
    if request.method == "POST":

        files = get_files()
        selected_base = request.get_json()["mybase"]
        session["CURRENT_FILE"] = get_name_file(
            selected_base, "get"
        )  # get the session value

        if session["CURRENT_FILE"] not in files:  # create new file
            session["CURRENT_FILE"] = "../Data/" + session["CURRENT_FILE"]
            if session["CURRENT_FILE"].endswith(".json") == False:
                session["CURRENT_FILE"] = session["CURRENT_FILE"] + ".json"
            with open(session["CURRENT_FILE"], "w") as new_file:
                new_file.write("[]")

        return {"status": "success"}

    elif request.method == "GET":

        files = get_files()
        paths = get_name_file(files, "split")
        return jsonify(sorted(paths))


@app.route("/ped", methods=["GET", "POST"])
def all_peds():
    if request.method == "POST":
        post_data = request.get_json()
        log.debug(f"/ped POST: {post_data}")
        with open(session["CURRENT_FILE"], "w") as PEDS:
            PEDS.write(json.dumps(post_data))
        return {"status": "success"}

    elif request.method == "GET":
        log.debug(f"session:{session}")
        with open(session.get("CURRENT_FILE"), "r") as PEDS:
            data = PEDS.read()
        return data

    else:
        raise NotImplementedError("Only GET and POST requests implemented for /ped")


@app.route("/upload", methods=["POST", "GET"])
def upload_file():
    if request.method == "POST":
        post_data = request.files
        id_list = []

        if "file" not in request.files:
            error = "Import error : No file imported"
            return error

        lines_list, extension = get_lines_content(post_data)
        separator = check_extension(extension, lines_list[0])
        if separator.startswith("Import"):
            error = separator
            return error
        if isinstance(lines_list[0], list):
            file_as_list = lines_list
        else:
            if separator == "xlsx":
                if "\t" in lines_list[0]:
                    separator = "\t"
                else:
                    separator = ","
            file_as_list = get_rows_list(lines_list, separator)
            log.debug(f"files_as_list:{file_as_list}")
            if isinstance(file_as_list, str) == True:
                error = file_as_list
                return error
        file_list, list_col_order = get_columns(file_as_list, extension)
        if list_col_order == None:
            error = file_list
            return error
        dict_list = fill_dict(file_list, list_col_order)
        peds_merged = merge_peds(dict_list)

        # unique ids
        for i in range(len(peds_merged)):
            id_list.append(peds_merged[i]["id"])
        if len(set(id_list)) != len(id_list):
            error = "Import error : IDs are not unique."
            return error

        peds_merged = check_fam_id(peds_merged)

        log.debug("end upload")
        return jsonify(peds_merged)


@app.route("/download", methods=["GET", "POST"])
def download_file():
    import tempfile

    tmp_dir = tempfile.gettempdir()
    if request.method == "POST":
        post_data = request.get_json()
        with open(session["CURRENT_FILE"], "r") as input:
            data = json.load(input)
        if post_data["typefile"] == "Ped file":

            with open(os.path.join(tmp_dir, "download.ped"), "w") as output:
                print(
                    "#Family ID",
                    "Individual ID",
                    "Paternal ID",
                    "Maternal ID",
                    "Sex",
                    "Phenotype",
                    file=output,
                    sep="\t",
                )

                for line in data:
                    line = ped_code(line)

                    print(
                        line["famID"],
                        line["id"],
                        line["paternalID"],
                        line["maternalID"],
                        line["sex"],
                        line["phenotype"],
                        file=output,
                        sep="\t",
                    )

        if post_data["typefile"] == "Advanced Ped file":
            log.debug(" Advanced Ped file if")
            with open(os.path.join(tmp_dir, "download.ped"), "w") as output:
                print(
                    "#Family ID",
                    "Individual ID",
                    "Paternal ID",
                    "Maternal ID",
                    "Sex",
                    "Phenotype",
                    "Alias",
                    "HPOList",
                    "STARK Tags",
                    file=output,
                    sep="\t",
                )

                for line in data:
                    line = ped_code(line)
                    print(
                        line["famID"],
                        line["id"],
                        line["paternalID"],
                        line["maternalID"],
                        line["sex"],
                        line["phenotype"],
                        line["alias"],
                        ",".join(line["HPOList"]),
                        ",".join(line["starkTags"]),
                        file=output,
                        sep="\t",
                    )

        return send_file(os.path.join(tmp_dir, "download.ped"))


# sanity check route, la route du site backend ou il va chercher les infos
@app.route("/ping", methods=["POST"])
def ping_pong():
    post_data = request.get_json()
    if "MEDINA Solène !" in post_data["msg"]:
        res = "NICAISE Samuel !"
    else:
        res = "MEDINA Solène !"
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4280, debug=True)
