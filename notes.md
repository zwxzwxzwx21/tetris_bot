with new window that shows how algorythm work i would like to add some things that may improve the clarity of how things work:
- have a small game window like, 360x640 for example, you have some modes on the left like:
     - "random" - which  just places pieces and clears lines, singles,doubles whatever currect algorythm has to offer
     - "spins" - disables or enables usage of spins
     - "holds" - disables or enables usage of holds
     - "PC mode" - bot takes perfect clears only (disabling it would make the bot just not take them ever)
- can add custom test modes like "4 wide" when the bot upstacks and tries to 20 combo down, or just something like, you have unlimited
left and right garbage and just make the bot try clearing as much combo as possible (preferably indefinitely) - REQUIRES SPINS

approaching APM and combo table:
i think the best idea would be to simply create some testcases (can finally use that stupid test folder ive created) as in:
use combo downstackpractice and just copy some maps from there (its a website to practice tetris downstack)
and then just give it to the bot to find either pc (as that is the gamemode in that webside) or jsut highest apm in one combo, for example:
give it a task to find the most amountn of attack within 5 pieces and see what happens, if it wont find a solution then expand the search and just fuck around really lol

# keep track of when a next piece when appear, when you place o piece on empty board, next o piece wont appear in at least 7 pieces 
^ this idea seems to be more suitable for AI not a bot, however i feel like in very late stage of developemnt, it could be implemented like, you dont upstack when i piece is deep into queue or whatever, but with depth bigger than one bag, seems useless (ie. wont really make the bot play better i think)

TODO type shit:

(those below actually more important)
- one thing in the code i noticed, bruteforcing o piece (unsure about other pieces)
starts with index ['O_x0_flat'] while next one is ['O_x2_flat'], check combo_attack_test.py to see board state, it could be issue because parsing movements can be fucked if x value (which is the number in name) seems off fsr


maybe split the BoardRealTimeView.py a bit so its not that clumped up, i think even when we move to TETR.IO it still could matter to have better view on what
is actually happening in console vs in game, but yeah its not also that this function will have literally everything, its just display and some options, can be
left in one file imo (unless someone smarter thinks otherwise)

