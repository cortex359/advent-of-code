namespace aoc_csharp_2022;

public class Day02 : Day
{
    public override void Run(string[] lines)
    {
        int toalScore = 0;
        foreach (string l in lines)
        {
            Round r = new Round(l, true);
            toalScore += r.score;
        }

        Console.WriteLine($"Part I: Total Score:  {toalScore}");
        
        toalScore = 0;
        foreach (string l in lines)
        {
            Round r = new Round(l, false);
            toalScore += r.score;
        }
        Console.WriteLine($"Part II: Total Score: {toalScore}");
    }

    class Round
    {
        public int score = 0;

        private int scoreVar1(string opponent, string me)
        {
            int score = 0;
            switch (me)
            {
                case "X":
                    score += 1; // Rock
                    score += opponent == "A" ? 3 : opponent == "C" ? 6 : 0;
                    break;
                case "Y":
                    score += 2; // Paper
                    score += opponent == "B" ? 3 : opponent == "A" ? 6 : 0;
                    break;
                case "Z":
                    score += 3; // Scissors
                    score += opponent == "C" ? 3 : opponent == "B" ? 6 : 0;
                    break;
            }
            return score;
        }
        
        private int scoreVar2(string opponent, string outcome)
        {
            int score = 0;
            // 1 for Rock, 2 for Paper, and 3 for Scissors
            switch (outcome)
            {
                case "X":
                    // loose
                    score += opponent == "A" ? 3 : opponent == "B" ? 1 : 2;
                    break;
                case "Y":
                    score += 3; // draw
                    score += opponent == "A" ? 1 : opponent == "B" ? 2 : 3;
                    break;
                case "Z":
                    score += 6; // win
                    score += opponent == "A" ? 2 : opponent == "B" ? 3 : 1;
                    break;
            }
            return score;
        }
        
        public Round(string l, bool var1)
        {
            string opponent = l.Split()[0]; // A B C
            string col2     = l.Split()[1]; // X Y Z

            if (var1)
            {
                score = scoreVar1(opponent, col2);
            }
            else
            {
                score = scoreVar2(opponent, col2);
            }
        }
    }
}