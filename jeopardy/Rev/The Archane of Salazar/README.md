# The Archane of Salazar

aseng

---

## Flag

```
LKSN{at_last_you_have_found_your_way_to_get_the_trophy_of_arcane_woop_woop!}
```

## Description

Only the one with the LKSN trophy will get the flag through the secret codes which you can control. Once you figured it out, connect to the server and gives us your best codes and the king will give you the flag!

`nc <ip> <port>`

## Difficulty
`medium-hard`

## Hints
* Bagaimana cara menganalisa secara dinamis pada ELF file?

## Tags
`ELF`

## Deployment

```
# In the deploy folder

docker build -t dedebugbug . 
docker run -p 37868:37868 -d -it dedebugbug
```