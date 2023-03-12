using System.Security.Cryptography;
using System.Text;

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
    
    private string ConvDigit(int d)
    {
        // 2  1  0  -   =
        // 2  1  0 -1  -2
        switch (d)
        {
            case 2:
            case 1:
            case 0:
                return "" + d;
                break;
            case -1:
                return "-";
                break;
            case -2:
                return "=";
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

    private String ConvToSNAFU(long dec)
    {
        return ConvTo5(dec).Replace("3", "1=").Replace("4", "1-");
    }
    
    private String ConvTo5(long dec)
    {
        long div = dec, rest = 0l;
        StringBuilder sb = new StringBuilder();
        do
        {
            rest = div % 5;
            div = (long)div / 5;
            sb.Insert(0, rest);
        } while (div > 0);
        return sb.ToString();
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

        // _ = ConvToSNAFU(totalSum);
        for (int i = 1; i < 101; i++)
        {
            Console.WriteLine($"{i,4} {ConvTo5(i),8} {ConvToSNAFU(i),12}");
        }
    }
}