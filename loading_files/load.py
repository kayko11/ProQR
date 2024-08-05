import requests
import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean, Text, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.mysql import insert

# Database configuration
DATABASE_URI = 'mysql+pymysql://root:admin@localhost:3306/mydb'

# Initialize database connection
engine = create_engine(DATABASE_URI, echo=True)

# Define the base class for declarative models
Base = declarative_base()

# Define the Notices model
class Notices(Base):
    __tablename__ = 'notices'
    id = Column(String(255), primary_key=True)
    parentId = Column(String(255), nullable=True)
    noticeIdentifier = Column(String(255))
    title = Column(Text)
    description = Column(Text)
    cpvDescription = Column(Text)
    cpvDescriptionExpanded = Column(Text)
    publishedDate = Column(DateTime)
    deadlineDate = Column(DateTime, nullable=True)
    awardedDate = Column(DateTime, nullable=True)
    awardedValue = Column(Float, nullable=True)
    awardedSupplier = Column(String(255), nullable=True)
    approachMarketDate = Column(DateTime, nullable=True)
    valueLow = Column(Float, nullable=True)
    valueHigh = Column(Float, nullable=True)
    postcode = Column(String(255), nullable=True)
    coordinates = Column(String(255), nullable=True)
    isSubNotice = Column(Boolean, nullable=True)
    noticeType = Column(String(255), nullable=True)
    noticeStatus = Column(String(255), nullable=True)
    isSuitableForSme = Column(Boolean, nullable=True)
    isSuitableForVco = Column(Boolean, nullable=True)
    awardedToSme = Column(Boolean, nullable=True)
    awardedToVcse = Column(Boolean, nullable=True)
    lastNotifableUpdate = Column(DateTime, nullable=True)
    organisationName = Column(String(255), nullable=True)
    sector = Column(String(255), nullable=True)
    cpvCodes = Column(String(255), nullable=True)
    cpvCodesExtended = Column(String(255), nullable=True)
    region = Column(String(255), nullable=True)
    regionText = Column(Text, nullable=True)
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)
    size = Column(Integer, nullable=True)

# Create the notices table
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Define the function to generate date ranges
def generate_date_ranges(start_date, end_date, interval_months):
    ranges = []
    current_start = start_date
    while current_start < end_date:
        current_end = current_start + relativedelta(months=interval_months)
        if current_end > end_date:
            current_end = end_date
        ranges.append((current_start, current_end))
        current_start = current_end
    return ranges

# Set the date range and other parameters
start_date = datetime.datetime(2019, 1, 1)
end_date = datetime.datetime(2024, 6, 30)
interval_months = 6
value_from = 10000000.00
value_to = 200000000000.00
size = 1000

date_ranges = generate_date_ranges(start_date, end_date, interval_months)

# Iterate over the date ranges and make requests
for published_from, published_to in date_ranges:
    url = f"https://www.contractsfinder.service.gov.uk/api/rest/2/search_notices/json"
    params = {
        'publishedFrom': published_from.strftime('%Y-%m-%d'),
        'publishedTo': published_to.strftime('%Y-%m-%d'),
        'size': size,
        'valueFrom': value_from,
        'valueTo': value_to
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    for notice in data['results']:
        notice_record = {
            'id': notice.get('id'),
            'parentId': notice.get('parentId'),
            'noticeIdentifier': notice.get('noticeIdentifier'),
            'title': notice.get('title'),
            'description': notice.get('description'),
            'cpvDescription': notice.get('cpvDescription'),
            'cpvDescriptionExpanded': notice.get('cpvDescriptionExpanded'),
            'publishedDate': notice.get('publishedDate'),
            'deadlineDate': notice.get('deadlineDate'),
            'awardedDate': notice.get('awardedDate'),
            'awardedValue': notice.get('awardedValue'),
            'awardedSupplier': notice.get('awardedSupplier'),
            'approachMarketDate': notice.get('approachMarketDate'),
            'valueLow': notice.get('valueLow'),
            'valueHigh': notice.get('valueHigh'),
            'postcode': notice.get('postcode'),
            'coordinates': notice.get('coordinates'),
            'isSubNotice': notice.get('isSubNotice'),
            'noticeType': notice.get('noticeType'),
            'noticeStatus': notice.get('noticeStatus'),
            'isSuitableForSme': notice.get('isSuitableForSme'),
            'isSuitableForVco': notice.get('isSuitableForVco'),
            'awardedToSme': notice.get('awardedToSme'),
            'awardedToVcse': notice.get('awardedToVcse'),
            'lastNotifableUpdate': notice.get('lastNotifableUpdate'),
            'organisationName': notice.get('organisationName'),
            'sector': notice.get('sector'),
            'cpvCodes': notice.get('cpvCodes'),
            'cpvCodesExtended': notice.get('cpvCodesExtended'),
            'region': notice.get('region'),
            'regionText': notice.get('regionText'),
            'start': notice.get('start'),
            'end': notice.get('end'),
            'size': size  # Ensure size is included
        }

        stmt = insert(Notices).values(notice_record)
        stmt = stmt.on_duplicate_key_update(
            parentId=stmt.inserted.parentId,
            noticeIdentifier=stmt.inserted.noticeIdentifier,
            title=stmt.inserted.title,
            description=stmt.inserted.description,
            cpvDescription=stmt.inserted.cpvDescription,
            cpvDescriptionExpanded=stmt.inserted.cpvDescriptionExpanded,
            publishedDate=stmt.inserted.publishedDate,
            deadlineDate=stmt.inserted.deadlineDate,
            awardedDate=stmt.inserted.awardedDate,
            awardedValue=stmt.inserted.awardedValue,
            awardedSupplier=stmt.inserted.awardedSupplier,
            approachMarketDate=stmt.inserted.approachMarketDate,
            valueLow=stmt.inserted.valueLow,
            valueHigh=stmt.inserted.valueHigh,
            postcode=stmt.inserted.postcode,
            coordinates=stmt.inserted.coordinates,
            isSubNotice=stmt.inserted.isSubNotice,
            noticeType=stmt.inserted.noticeType,
            noticeStatus=stmt.inserted.noticeStatus,
            isSuitableForSme=stmt.inserted.isSuitableForSme,
            isSuitableForVco=stmt.inserted.isSuitableForVco,
            awardedToSme=stmt.inserted.awardedToSme,
            awardedToVcse=stmt.inserted.awardedToVcse,
            lastNotifableUpdate=stmt.inserted.lastNotifableUpdate,
            organisationName=stmt.inserted.organisationName,
            sector=stmt.inserted.sector,
            cpvCodes=stmt.inserted.cpvCodes,
            cpvCodesExtended=stmt.inserted.cpvCodesExtended,
            region=stmt.inserted.region,
            regionText=stmt.inserted.regionText,
            start=stmt.inserted.start,
            end=stmt.inserted.end,
            size=stmt.inserted.size  # Ensure size is updated
        )

        session.execute(stmt)

# Commit the session to save data to the database
session.commit()
