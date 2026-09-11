using System.Diagnostics;

namespace Chris.ActivityLab;

public static class ActivityLab
{
    /// <summary>TODO [DN-ACT-SOURCE-01]: create named ActivitySource.</summary>
    public static ActivitySource CreateSource(string name)
    {
        throw new NotImplementedException("DN-ACT-SOURCE-01");
    }

    /// <summary>TODO [DN-ACT-SPAN-02]: start span with module tag.</summary>
    public static Activity? StartWorkSpan(ActivitySource src, string op)
    {
        throw new NotImplementedException("DN-ACT-SPAN-02");
    }

    /// <summary>TODO [DN-ACT-EXPORT-03]: textual span summary.</summary>
    public static string ExportSpanSummary(Activity? act)
    {
        throw new NotImplementedException("DN-ACT-EXPORT-03");
    }
}
