import os
from ... import geotable as pdio
from ...fileio import FileIO as psopen
import unittest as ut
from .... import examples as pysal_examples

import platform
import shapely

try:
    import sqlalchemy

    missing_sql = False
except ImportError:
    missing_sql = True


windows = platform.system() == "Windows"


@ut.skipIf(windows, "Skipping Windows due to `PermissionError`.")
@ut.skipIf(missing_sql, f"Missing dependency: SQLAlchemy ({missing_sql}).")
class Test_sqlite_reader(ut.TestCase):
    def setUp(self):
        path = pysal_examples.get_path("new_haven_merged.dbf")
        if path is None:
            pysal_examples.load_example("newHaven")
            path = pysal_examples.get_path("new_haven_merged.dbf")
        df = pdio.read_files(path)
        df["GEOMETRY"] = shapely.to_wkb(shapely.points(df["geometry"].values.tolist()))
        # This is a hack to not have to worry about a custom point type in the DB
        del df["geometry"]
        self.dbf = "iohandlers_test_db.db"
        engine = sqlalchemy.create_engine(f"sqlite:///{self.dbf}")
        self.conn = engine.connect()
        df.to_sql(
            "newhaven",
            self.conn,
            index=True,
            dtype={
                "date": sqlalchemy.types.UnicodeText,  # Should convert the df date into a true date object, just a hack again
                "dataset": sqlalchemy.types.UnicodeText,
                "street": sqlalchemy.types.UnicodeText,
                "intersection": sqlalchemy.types.UnicodeText,
                "time": sqlalchemy.types.UnicodeText,  # As above re: date
                "GEOMETRY": sqlalchemy.types.BLOB,
            },
        )  # This is converted to TEXT as lowest type common sqlite

    def test_deserialize(self):
        db = psopen(f"sqlite:///{self.dbf}")
        self.assertEqual(db.tables, ["newhaven"])

        gj = db._get_gjson("newhaven")
        self.assertEqual(gj["type"], "FeatureCollection")

        self.conn.close()

        os.remove(self.dbf)


if __name__ == "__main__":
    ut.main()
