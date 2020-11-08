## Raspberry Pi Poll API LED Controller

#### A library to control LEDs from poll based input.

---
## Description
*A poll in this instance is an object with boolean votes.*

*e.g* `"Do you like tacos? (50 for, 3 against")`

The current application fetches poll data from a Spring Rest API and converts the sum of the votes into respective ratios
for each answer. --> `50 for, 3 against = 94% for, 5% against`. The application uses these values to
control two parallel strips of red and green LEDs (with PWM), where the amount of LEDs lighting up equals
the ratio of votes.

#### Pin layout

<img src="https://i.imgur.com/OLPCoKe.png" height="600">

![](https://via.placeholder.com/15/6FFF5C/000000?text=+)  `pins` : used to control green LEDs.

![](https://via.placeholder.com/15/EB1C20/000000?text=+)  `pins` : used to control red LEDs.

![](https://via.placeholder.com/15/FFF129/000000?text=+)  `pins` : used for indicator light when transitioning between polls.

![](https://via.placeholder.com/15/030202/000000?text=+)  `pins` : used to short circuit.

#### Circuit diagram
**-- COMING SOON --**

---

## How to use

```
t = VotesToLeds()
first_votes = Votes(50, 50)
t.fade_to_poll(votes)
sleep(4)
sec_votes = Votes(1,1000)
t.fade_to_poll(sec_votes)
sleep(5)
```

---


*keywords: Spring, RPi, IoT*
