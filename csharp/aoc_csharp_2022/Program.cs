namespace aoc_csharp_2022;

public abstract class Day
{
    public string Name
    {
        get => this.GetType().Name;
    }
    public abstract void Run(string[] lines);
}

public class Program
{
    //public static readonly string ProjectDir = GetProjectDir("aoc_csharp_2022");
    private const string ProjectName = "aoc_csharp_2022";
    
    public static void Main(string[] args)
    {
        if (args.Length == 0)
        {
            Day day = new Day25();

            string input = Path.Join(ProjectDir, day.Name, "input");
            string[] lines = File.ReadAllLines(input);

            day.Run(lines);
        }
    }

    public static string ProjectDir
    {
        get => GetProjectDir(ProjectName);
    }
    
    private static string GetProjectDir(string projectName)
    {
        string path = Directory.GetCurrentDirectory();

        string[] pathElements = Path.GetFullPath(path).Split(Path.DirectorySeparatorChar);
        string projectDir = "" + Path.DirectorySeparatorChar;
        foreach (string p in pathElements)
        {
            projectDir = Path.Join(projectDir, p);
            if (p.Equals(projectName))
                break;
        }

        return projectDir;
    }
}
