using System.Diagnostics;

namespace Chris.ActivityLab;

public static class ActivityLab
{
    /// <summary>Creates named ActivitySource.</summary>
    public static ActivitySource CreateSource(string name)
    {
        // PEDAGOGY-SOLUTION: DN-ACT-SOURCE-01
        return new ActivitySource(name);
    }

    /// <summary>Starts span with module tag.</summary>
    public static Activity? StartWorkSpan(ActivitySource src, string op)
    {
        // PEDAGOGY-SOLUTION: DN-ACT-SPAN-02
        var act = src.StartActivity(op);
        act?.SetTag("module", "activity_source_span");
        return act;
    }

    /// <summary>Textual span summary export.</summary>
    public static string ExportSpanSummary(Activity? act)
    {
        // PEDAGOGY-SOLUTION: DN-ACT-EXPORT-03
        if (act is null) return "null";
        return $"{act.OperationName}|{act.GetTagItem("module")}";
    }
}
