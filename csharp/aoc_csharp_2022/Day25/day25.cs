using System.Security.Cryptography;

namespace aoc_csharp_2022;

public class Day25 : Day
{
    private int ConvDigit(string s)
    {
        // 2  1  0  -   =
        // 2  1  0 -1  -2
        switch (s)
        {
            case "2":
            case "1":
            case "0":
                return int.Parse(s);
                break;
            case "-":
                return -1;
                break;
            case "=":
                return -2;
                break;
            default:
                throw new ArithmeticException();
        }
    }
    
    private long ConvToDec(String line)
    {
        // … 5^3 5^2 5^1 5^0
        long dec = 0;
        int power = 0;
        for (int i = line.Length -1; i >= 0; i--)
        {
            dec += ConvDigit("" + line[i]) * (long) Math.Pow(5, power++);
        }

        return dec;
    }

    private String ConvToSNAFU(int dec)
    {
        return "";
    }
    
    public override void Run(string[] lines)
    {
        long totalSum = 0;        
        foreach (string s in lines)
        {
            Console.WriteLine("{0,30} {1,16:d}", s, ConvToDec(s));
            totalSum += ConvToDec(s);
        }

        Console.WriteLine($"Summe: {totalSum}");
    }
}