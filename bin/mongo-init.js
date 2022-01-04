db.createUser(
    {
        user: "vozyadmin",
        pwd: "vozy",
        roles: [
            {
                role: "readWrite",
                db: "vozydb"
            }
        ]
    }
);