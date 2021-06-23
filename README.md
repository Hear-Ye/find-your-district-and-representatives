# Find Your District

Created by: [Andrew Chen Wang](https://github.com/Andrew-Chen-Wang)

Created on: 23 June 2021

This Starlette app, given geographic coordinates,
gets a user their coordinates

---
### Usage

Install: `pip install -r requirements/local.txt`

Run: `uvicorn src.app:app`

---
### License

I designed this quick web for the Hear Ye app.
This repository is licensed under Apache 2.0.
You can view the full license in the [LICENSE](./LICENSE)
file.

This app also uses 
[Andrew-Chen-Wang/district-autoupdate](https://github.com/Andrew-Chen-Wang/district-autoupdate)
and the [unitedstates GitHub organization](https://github.com/unitedstates)
(they are not affiliated with the United States government)
to provide this data. Really appreciate it!


---
### TODOs

- Automate deployment along with cron job
- Add "find representative" here, as well
  for the sake of open source, open knowledge.
  The exception is that this route will not be
  publicly available I think since I don't want
  to crash the server. We'll see :)
- Add throttling by IP address. It's really not
  necessary for an attacker to come unless they
  have the sole mission of ruining the server.
