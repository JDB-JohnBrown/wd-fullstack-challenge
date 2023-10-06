CREATE TABLE user (
    user_id INTEGER, 
    username TEXT, 
    passw TEXT
);

CREATE TABLE user_session(
    user_session_id INTEGER, 
    user_id INTEGER, 
    login_date INTEGER, /*UNIX Time, seconds since 1970-01-01 00:00:00 UTC*/ 
    expire_date INTEGER, /*UNIX Time, seconds since 1970-01-01 00:00:00 UTC*/ 
    logged_out INTEGER, /*BOOLEAN; FALSE=0; TRUE=1*/
    jwToken TEXT, 
    url TEXT, 
    logout_date INTEGER /*UNIX Time, seconds since 1970-01-01 00:00:00 UTC*/ 
);

CREATE TABLE property (
    property_id INTEGER PRIMARY KEY,
    full_address TEXT, 
    longitude REAL, /*Maybe I should do text?*/
    latitude REAL,
    zip TEXT, /*Definitely need to do text here*/
    /*I don't know what data form the rest of these we actually want to keep... 
    let's just keep them all*/
    rec_type TEXT,
    pin TEXT,
    ovacls TEXT,
    class_description TEXT,
    current_land TEXT,
    current_building TEXT,
    current_total TEXT,
    estimated_market_value TEXT,
    prior_land TEXT,
    prior_building TEXT,
    prior_total TEXT,
    pprior_land TEXT,
    pprior_building TEXT,
    pprior_total TEXT,
    pprior_year TEXT,
    town TEXT,
    volume TEXT,
    loc TEXT,
    tax_code TEXT,
    neighborhood TEXT,
    houseno TEXT,
    dir TEXT,
    street TEXT,
    suffix TEXT,
    apt TEXT,
    city TEXT,
    res_type TEXT,
    bldg_use TEXT,
    apt_desc TEXT,
    comm_units TEXT,
    ext_desc TEXT,
    full_bath TEXT,
    half_bath TEXT,
    bsmt_desc TEXT,
    attic_desc TEXT,
    ac TEXT,
    fireplace TEXT,
    gar_desc TEXT,
    age TEXT,
    building_sq_ft TEXT,
    land_sq_ft TEXT,
    bldg_sf TEXT,
    units_tot TEXT,
    multi_sale TEXT,
    deed_type TEXT,
    sale_date TEXT,
    sale_amount TEXT,
    appcnt TEXT,
    appeal_a TEXT,
    appeal_a_status TEXT,
    appeal_a_result TEXT,
    appeal_a_reason TEXT,
    appeal_a_pin_result TEXT
    appeal_a_propav TEXT,
    appeal_a_currav TEXT,
    appeal_a_resltdate TEXT
);

CREATE TABLE user_property_link (
    user_id INTEGER, 
    property_id INTEGER, 
    create_date INTEGER, /*UNIX Time, seconds since 1970-01-01 00:00:00 UTC*/ 
    FOREIGN KEY(user_id) REFERENCES user(user_id),
    FOREIGN KEY(property_id) REFERENCES property(property_id)
);