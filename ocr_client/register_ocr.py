import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import argparse
from app.db import OCR


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', type=str, required=True, help="Database to register OCR engines.")
    parser.add_argument('-r', '--replace', action="store_true", help="Replace all OCR engines.")
    args = parser.parse_args()
    return args


ocr_engines = [
    {"name": "IMPACT", "description": "IMPACT"},
    {"name": "DTA", "description": "DTA"},
    {"name": "IMPACT_LN", "description": "Net for LIDOVE NOVINY"}
]


def main():
    args = parseargs()

    database_url = 'sqlite:///' + args.database
    engine = create_engine(database_url, convert_unicode=True, connect_args={'check_same_thread': False})
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))

    if args.replace:
        for db_ocr in db_session.query(OCR).all():
            db_ocr.active = False
        db_session.commit()

    for ocr in ocr_engines:
        if db_session.query(OCR).filter(OCR.name == ocr['name']).filter(OCR.active == True).first() is None:
            db_ocr = OCR(**ocr)
            db_session.add(db_ocr)
            print('ADDED ', ocr)
        else:
            print('SKIPPING', ocr)

    db_session.commit()


if __name__ == '__main__':
    sys.exit(main())
