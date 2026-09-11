using System.Diagnostics;
using Chris.ActivityLab;
using Xunit;

namespace Chris.ActivityLab.Tests;

public class ActivityTests
{
    private static ActivityListener CreateListener(string sourceName)
    {
        return new ActivityListener
        {
            ShouldListenTo = src => src.Name == sourceName,
            Sample = (ref ActivityCreationOptions<ActivityContext> _) => ActivitySamplingResult.AllData,
        };
    }

    // Caso 1: DN-ACT-SOURCE-01
    // PEDAGOGY-TEST: DN-ACT-SOURCE-01
    [Fact]
    public void Caso1_CreateSource_Name()
    {
        using var src = ActivityLab.CreateSource("chris.lab");
        Assert.Equal("chris.lab", src.Name);
    }

    // Caso 2: DN-ACT-SPAN-02
    // PEDAGOGY-TEST: DN-ACT-SPAN-02
    [Fact]
    public void Caso2_StartWorkSpan_Tag()
    {
        using var listener = CreateListener("chris.lab");
        ActivitySource.AddActivityListener(listener);
        using var src = ActivityLab.CreateSource("chris.lab");
        using var act = ActivityLab.StartWorkSpan(src, "work");
        Assert.NotNull(act);
        Assert.Equal("activity_source_span", act!.GetTagItem("module"));
    }

    // Caso 3: DN-ACT-EXPORT-03
    // PEDAGOGY-TEST: DN-ACT-EXPORT-03
    [Fact]
    public void Caso3_ExportSummary()
    {
        using var listener = CreateListener("chris.lab");
        ActivitySource.AddActivityListener(listener);
        using var src = ActivityLab.CreateSource("chris.lab");
        using var act = ActivityLab.StartWorkSpan(src, "work");
        var s = ActivityLab.ExportSpanSummary(act);
        Assert.Equal("work|activity_source_span", s);
    }
}
