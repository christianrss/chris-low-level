namespace Chris.JitLab;
public abstract class Animal { public abstract string Speak(); }
public class Dog : Animal { public override string Speak() => "woof"; }
public static class CallSite {
    public static string Dispatch(Animal a) {
        // PEDAGOGY-SOLUTION: D9-DN-VIRT
        return a.Speak();
    }
    public static string DevirtDog(Dog d) {
        // PEDAGOGY-SOLUTION: D9-DN-DEVIRT
        return d.Speak();
    }
    public static bool IsExactDog(Animal a) {
        // PEDAGOGY-SOLUTION: D9-DN-TYPE
        return a.GetType() == typeof(Dog);
    }
}
