using System.Runtime.InteropServices;
namespace Chris.PinnedLab;
public static class Pinned {
    public static int SumPinned(byte[] data) {
        // PEDAGOGY-SOLUTION: D8-DN-PIN
        var handle = GCHandle.Alloc(data, GCHandleType.Pinned);
        try {
            // PEDAGOGY-SOLUTION: D8-DN-LEN
            int n = data.Length;
            // PEDAGOGY-SOLUTION: D8-DN-SUM
            int s = 0;
            for (int i = 0; i < n; i++) s += data[i];
            return s;
        } finally {
            handle.Free();
        }
    }
}
