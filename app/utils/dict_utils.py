def orm_to_dict(orm: any) -> dict:
    d = {}
    for p in orm.__table__.columns:
        d[p.name] = getattr(orm, p.name)
    return d