package com.bench.runner;

import com.bench.matrix.Matrix;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.results.RunResult;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.*;
import java.util.Collection;
import java.util.Locale;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.SECONDS)
@Warmup(iterations = 1)
@Measurement(iterations = 1)
@Fork(1)
public class RunBench {

    private static final String LANGUAGE = "java";

    @State(Scope.Benchmark)
    public static class MatrixState {
        @Param({"64"})
        public int n;

        public double[][] A;
        public double[][] B;

        @Setup(Level.Trial)
        public void setup() {
            A = Matrix.randomMatrix(n, 1234L);
            B = Matrix.randomMatrix(n, 5678L);
        }
    }

    @Benchmark
    public double[][] benchmarkMatrixMultiply(MatrixState state) {
        return Matrix.matmulBasic(state.A, state.B);
    }

    public static void main(String[] args) throws RunnerException, IOException {
        if (args.length != 2) {
            System.err.println("Usage: java -jar benchmarks-java-jar-with-dependencies.jar <matrix_size> <rounds>");
            System.exit(1);
        }

        Locale.setDefault(Locale.ROOT);

        final int n = Integer.parseInt(args[0]);
        final int rounds = Integer.parseInt(args[1]);

        Path projectRoot = Paths.get("").toAbsolutePath();
        Path javaRoot = projectRoot.resolve("benchmarks_java");
        Path resultsDir = javaRoot.resolve("results");
        Path csvPath = resultsDir.resolve("matrix_bench_java.csv");
        Files.createDirectories(resultsDir);
        ensureHeader(csvPath);

        Options opt = new OptionsBuilder()
                .include(RunBench.class.getSimpleName())
                .param("n", String.valueOf(n))
                .warmupIterations(0)
                .measurementIterations(rounds)
                .forks(1)
                .build();

        Collection<RunResult> results = new Runner(opt).run();

        long usedBytes = usedHeapBytes();
        double memMB = usedBytes / (1024.0 * 1024.0);

        for (RunResult r : results) {
            double timePerOp = r.getPrimaryResult().getScore(); 
            appendCsv(csvPath, LANGUAGE, n, timePerOp, memMB);
        }
    }

    private static long usedHeapBytes() {
        Runtime rt = Runtime.getRuntime();
        return rt.totalMemory() - rt.freeMemory();
    }

    private static void ensureHeader(Path csvPath) throws IOException {
        if (Files.notExists(csvPath) || Files.size(csvPath) == 0) {
            try (BufferedWriter w = Files.newBufferedWriter(csvPath)) {
                w.write("language,size,execution_time_s,memory_usage_mb");
                w.newLine();
            }
        }
    }

    private static void appendCsv(Path csvPath, String language, int size, double seconds, double memMB) throws IOException {
        try (BufferedWriter w = Files.newBufferedWriter(csvPath, StandardOpenOption.APPEND)) {
            w.write(String.format(Locale.ROOT, "%s,%d,%.6f,%.2f", language, size, seconds, memMB));
            w.newLine();
        }
    }
}
