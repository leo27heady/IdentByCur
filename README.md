# Identification
README.md

User identification by cursor movement

Program description

Task: Needs to recognize in 10 movements of the cursor whether the person who moves the cursor is the owner of the laptop.<br>
Created a program in which the user is recognize (authenticate) by cursor movements. To recognize the user, you needed to click 10 times on the squares that appear alternately in random places. <br>

<figure>
  <img src="https://user-images.githubusercontent.com/45982614/98411973-c4d28b00-207f-11eb-96ad-6ce6b26bd5b4.png">
  <figcaption>Software display</figcaption>
</figure>

<br><br>
When the cursor moves, 5 parameters are calculated: 
- Speed 10% of the way
- Average speed
- Maximum speed
- Delay before pressing
- The standard deviation

All 10 movements are combined into a Pack (10x5 matrix), which will be user recognition:<br>
[[V10, V, Vm, tc, s], [V10, V, Vm, tc, s], ...]<br><br>
Then they are stored in files and grouped into folders corresponding to their users.<br>

<figure>
  <img src="https://user-images.githubusercontent.com/45982614/98414487-20067c80-2084-11eb-9551-97ef39d74e9b.png" width="400">
  <figcaption>Folder structure</figcaption>
</figure>
