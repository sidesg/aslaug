import os
import sqlite3
import subprocess
import shutil

class Analyser():
    def __init__(self, source: str, destination: str, arguments: dict):
        self.source_dir = source
        self.report_dir = destination
        self.csv_dir = os.path.join(destination, "csv_reports")
        self.log_dir = os.path.join(destination, "logs")
        self.bulkext_dir = os.path.join(destination, "bulk_extractor")
        self.sf_file = os.path.join(destination, "siegfried.csv")
        self.use_hash = False
        self.args = arguments
    
    @classmethod
    def new(cls, source: str, destination: str, **kwargs):
        args = {k: v for k, v in kwargs.items()}
        return cls(
            source,
            destination,
            args
        )

    def create_report_dir(self):
        if os.path.exists(self.report_dir):
            if not self.args.get("overwrite"):
                raise FileExistsError("Output directory already exists. To overwrite, use the -o/--overwrite option.")
            else:
                shutil.rmtree(self.report_dir)
        os.makedirs(self.report_dir)

    def _determine_hash_type(self) -> str:
        """Return hash_type value to use as argument for Siegfried

        Defaults to md5 if no or invalid user input.
        """
        HASH_CHOICES = ("sha1", "sha256", "sha512")
        if self.args.get("hash") and self.args.get("hash").lower() in HASH_CHOICES:
            return self.args.get("hash").lower()
        else:
            return "md5"

    def run_siegfried(self):
        """Run siegfried on directory: Writes results to self.sf_file location"""
        sf_command = 'sf -csv "%s" > "%s"' % (self.source_dir, self.sf_file)
        if self.use_hash:
            hash_type = self._determine_hash_type()
            sf_command = 'sf -csv -hash %s "%s" > "%s"' % (hash_type, self.source_dir, self.sf_file)
        if self.args.get("scanarchives",):
            sf_command = sf_command.replace("sf -csv", "sf -z -csv")
        if self.args.get("throttle"):
            sf_command = sf_command.replace("-csv -hash", "-csv -throttle 10ms -hash")
        if self.args.get("verbosesf"):
            sf_command = sf_command.replace(" -hash", " -log p,t -hash")
        
        subprocess.call(sf_command, shell=True)

    def create_html_report(self):
        ...

    def make_db(self) -> sqlite3.Connection:
        db = os.path.join(self.report_dir, "siegfried.sqlite")
        conn = sqlite3.connect(db)
        conn.text_factory = str
        return conn
    
    def load_sf_db(self, conn, csv=None):
        """If no csv argument is passed, method will use default self.sf_file"""
        if not csv:
            csv=self.sf_file
