# MouseTrap
When trapping mice in my attic or other places in the house I prefer to live trap and re-locate the waword animals to the woods.  The sad fact is that unless you check your traps several times a day, you are no longer live trapping.  Making a trip up into the attic several times per day just isn't practical for me so I created a technical solution.  The solution involves a simple magnetic switch installed on the mousetrap wired to an ESP32 microcontroller.  The controller is running a Python app that will keep checking the trap and send me text message when the trap is triggered.  

### Requurements:
- An ESP32 micro controller.  I am using the tinyPico: https://www.tinypico.com/
- A live mousetrap, this is the one I am using: https://www.amazon.com/UPGRADED-CaptSure-Release-Reusable-Hamsters/dp/B073GRKG88?maas=maas_adg_FB26FCFA5127E1405CECFEECE5B497E6_afap_abs&ref_=aa_maas&tag=maas&ref_=ast_sto_dp&th=1&psc=1&gclid=CjwKCAiA_omPBhBBEiwAcg7smZ350AD3WVfR6O5ZuehMiZ_nwMKNB6lywd6MmLKhmsrJp7Mui44c0RoCvooQAvD_BwE
- A magnetic switch installed on the exterior of the trap with a magnet placed on the door.  https://www.amazon.com/Gebildet-Normally-Induction-2-5mm%C3%9714mm-Multi-Use/dp/B07YFBQ4HS/ref=sr_1_9?crid=128US5I23LTG3&keywords=magnetic+switch+normally+open&qid=1642262989&sprefix=magnetic+switch%2Caps%2C103&sr=8-9

### Assembily:
I used an external magnetic switch to enable cleaning of the trap between uses.  The switch is glued in place with plastic glue and encased in hot glue to provide water resistance.  
I installed a barrel connector ~1ft from the trap to enable disconnection for cleaning.  A 10 ft cable runs from the trap to the ESP32 controller so that it can be loacated close to a power source.

### Usage:
1. Load files and update config.py with phone numbers and Twillow API keys.
2. Trigger debug mode by booting up with the trap closed.  In this mode the microcontroller LED will alternate between red and green depending on if the circuit is open or closed.  This is a great way to test and troubleshoot hardware setup.
3. Resetting the devise with the door open enters normal operation.  The program will wake up and check the circuit every 30 seconds.  If the circuit is closed, a green light will flash.  If the circuit is open (meaning the trap door closed), a yellow light will flash inidicating a Wifi connection is being made and a text message will be sent.  A message will only be sent one time, but the trap will continue to check circuit status.
