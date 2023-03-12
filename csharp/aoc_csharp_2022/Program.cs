namespace aoc_csharp_2022;

public class Program
{
    //public static readonly string ProjectDir = GetProjectDir("aoc_csharp_2022");
    private const string ProjectName = "aoc_csharp_2022";
    
    public static void Main(string[] args)
    {
        if (args.Length == 0)
        {
            string input = Path.Join(ProjectDir, nameof(Day01), "input");
            string[] lines = File.ReadAllLines(input);
            Day01.Run(lines);
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
