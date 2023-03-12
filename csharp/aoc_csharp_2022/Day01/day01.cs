namespace aoc_csharp_2022;

public class Day01 : Day
{
    public override void Run(string[] lines)
    {
        List<int> elves = new List<int>();
        int weight = 0;
        foreach (string l in lines)
        {
            if (l.Equals(""))
            {
                elves.Add(weight);
                weight = 0;
            }
            else
            {
                weight += Int32.Parse(l);
            }
        }
        elves.Add(weight);

        Console.WriteLine($"Max at {elves.Max()}");
        
        elves.Sort();

        int topThree = elves[^1] + elves[^2] + elves[^3];
        Console.WriteLine($"Top three sum {topThree}");
    }
}