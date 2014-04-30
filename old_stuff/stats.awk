
# Usage: awk -f stats.awk somefile.txt

BEGIN { 

  print FILENAME

  #initialize some variables
  maxlvl=0
  deaths=0
  turns=0
  maxTurns=0
  points=0
  maxPoints=0
  maxHP=0
  maxDeaths=0
  ascended=0
  maxTime=0
  ascensionTurns=0
  maxAscensionTurns=0
  leastAscensionTurns=100000000
  player_name="zomGreg"


  FS = ":" ;
  #print "zomGreg Nethack Summary" ;
  #print "=======================\n" ;

}

  #Get the total points
  {split($2,a,"="); total += a[2]}
  {split($2,a,"="); thisPoints=a[2]; if ( thisPoints > maxPoints ) maxPoints=thisPoints }
  
  # Level Stats
  {split($5,a,"="); totalLevel += a[2]}
  {split($5,m,"="); thislvl=m[2]; if ( thislvl > maxlvl ) maxlvl=thislvl }
  
  # This will print the running average of the average
  # dungeon level reached.
  #{print totalLevel/NR}

  # Turns
  {split($19,a,"="); totalTurns += a[2]}
  {split($19,m,"="); thisTurns=m[2]; if ( thisTurns > maxTurns ) maxTurns=thisTurns }

  # Max HP
  {split($7,m,"="); thisHP=m[2]; if ( thisHP > maxHP ) maxHP=thisHP }

  #Death Stats
  {split($8,a,"="); totalDeaths += a[2]}
  {split($8,a,"="); thisDeaths=a[2]; if ( thisDeaths > maxDeaths ) maxDeaths=thisDeaths }

  #Got Ascension?
  {split($17,a,"="); if ( a[2] == "ascended" ) ascended+=1 }
  {split($17,a,"="); if ( a[2] == "ascended" ) {split($19,a,"="); totalAscensionTurns+=a[2]}}

  # Find slowest Ascension
  {
  
    split($17,a,"="); if ( a[2] == "ascended" ) {

      split($19,a,"="); thisAscension=a[2]; 

      if ( thisAscension > maxAscensionTurns ) 

      {
        maxAscensionTurns=thisAscension 
      }
    }
  }

  # Find fastest Ascension
  {
  
    split($17,a,"="); if ( a[2] == "ascended" ) {

      split($19,a,"="); thisAscension=a[2]; 

      if ( thisAscension < leastAscensionTurns ) 

      {
        leastAscensionTurns=thisAscension 
      }
    }
  }

END { 

  printf "%13[ %s games ]\n", (NR)

  printf "\n%13[ %s ]\n", "Ascensions"

  printf "\n%-25s %s %2.3f %s\n", "Ascensions: ", ascended " (", ((ascended/NR)*100), "%)"
  printf "%-25s %s\n", "Average Turns/Ascension: ", totalAscensionTurns/ascended
  printf "%-25s %s\n", "Fastest Ascension: ", leastAscensionTurns
  printf "%-25s %s\n", "Slowest Ascension: ", maxAscensionTurns

  printf "\n%13[ %s ]\n", "The Numbers"
  printf "\n%-25s %s\n", "Total points: ", total
  printf "%-25s %d\n", "Average Score: ", total/NR
  printf "%-25s %s\n", "Maximum Score: ", maxPoints
  printf "%-25s %s\n", "Maximum HP: ", maxHP
  printf "%-25s %s\n", "Max Level: ", maxlvl
  printf "%-25s %2.2f\n", "Average Level Reached: ", totalLevel/NR
  printf "%-25s %s\n", "Total Turns: ", totalTurns
  printf "%-25s %s\n", "Maximum Turns: ", maxTurns
  printf "%-25s %d\n", "Average Turns per Game: ", totalTurns/NR
  printf "%-25s %s\n", "Total Deaths: ", totalDeaths
  printf "%-25s %s\n", "Max Deaths: ", maxDeaths
  printf "\n"
}
