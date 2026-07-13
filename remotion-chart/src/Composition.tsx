import {
  AbsoluteFill,
  Composition,
  Easing,
  interpolate,
  useCurrentFrame,
} from "remotion";

type ChartProps = {
  title: string;
  subtitle: string;
};

const chartData = [
  { label: "Mon", value: 42, color: "#6EE7F9" },
  { label: "Tue", value: 68, color: "#67D4FF" },
  { label: "Wed", value: 54, color: "#61B9FF" },
  { label: "Thu", value: 86, color: "#7C8CFF" },
  { label: "Fri", value: 73, color: "#A879FF" },
] as const;

const easeOut = Easing.bezier(0.16, 1, 0.3, 1);
const chartHeight = 520;

const Bar: React.FC<(typeof chartData)[number] & { index: number }> = ({
  label,
  value,
  color,
  index,
}) => {
  const frame = useCurrentFrame();
  const startFrame = 28 + index * 8;

  return (
    <div
      style={{
        alignItems: "center",
        display: "flex",
        flex: 1,
        flexDirection: "column",
        gap: 22,
        height: "100%",
        justifyContent: "flex-end",
      }}
    >
      <div
        style={{
          alignItems: "flex-end",
          display: "flex",
          height: chartHeight,
          justifyContent: "center",
          position: "relative",
          width: "100%",
        }}
      >
        <div
          style={{
            alignItems: "center",
            background: `linear-gradient(180deg, ${color}, ${color}B8)`,
            borderRadius: "28px 28px 12px 12px",
            boxShadow: `0 18px 60px ${color}42`,
            display: "flex",
            height: interpolate(
              frame,
              [startFrame, startFrame + 34],
              [0, (value / 100) * chartHeight],
              {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
                easing: easeOut,
              },
            ),
            justifyContent: "center",
            overflow: "hidden",
            width: 190,
          }}
        >
          <span
            style={{
              color: "#07111F",
              fontSize: 58,
              fontWeight: 800,
              opacity: interpolate(
                frame,
                [startFrame + 14, startFrame + 26],
                [0, 1],
                {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                },
              ),
              paddingTop: 28,
              placeSelf: "flex-start center",
            }}
          >
            {Math.round(
              interpolate(frame, [startFrame, startFrame + 34], [0, value], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
                easing: easeOut,
              }),
            )}
            %
          </span>
        </div>
      </div>
      <div
        style={{
          color: "#D9E5F5",
          fontSize: 40,
          fontWeight: 650,
          letterSpacing: "0.02em",
          opacity: interpolate(frame, [startFrame, startFrame + 18], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}
      >
        {label}
      </div>
    </div>
  );
};

export const FiveBarChart: React.FC<ChartProps> = ({ title, subtitle }) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(circle at 78% 12%, #1D3458 0%, #0A1628 36%, #050B14 78%)",
        color: "white",
        fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif",
        overflow: "hidden",
        padding: "104px 120px 92px",
      }}
    >
      <div
        style={{
          background: "#45D6E820",
          borderRadius: "50%",
          filter: "blur(90px)",
          height: 420,
          left: -160,
          position: "absolute",
          top: 260,
          width: 420,
        }}
      />

      <header
        style={{
          opacity: interpolate(frame, [0, 20], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: easeOut,
          }),
          translate: interpolate(frame, [0, 20], ["0px 28px", "0px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: easeOut,
          }),
        }}
      >
        <h1
          style={{
            fontSize: 92,
            fontWeight: 780,
            letterSpacing: "-0.045em",
            lineHeight: 1,
            margin: 0,
          }}
        >
          {title}
        </h1>
        <p
          style={{
            color: "#8FA8C6",
            fontSize: 38,
            fontWeight: 500,
            margin: "20px 0 0",
          }}
        >
          {subtitle}
        </p>
      </header>

      <div
        style={{
          alignItems: "flex-end",
          display: "flex",
          flex: 1,
          gap: 46,
          padding: "38px 36px 0",
          position: "relative",
        }}
      >
        {[25, 50, 75, 100].map((tick) => (
          <div
            key={tick}
            style={{
              background: "#C7D8EE16",
              bottom: 70 + (tick / 100) * chartHeight,
              height: 2,
              left: 0,
              position: "absolute",
              right: 0,
            }}
          />
        ))}
        {chartData.map((item, index) => (
          <Bar key={item.label} {...item} index={index} />
        ))}
      </div>
    </AbsoluteFill>
  );
};

export const FiveBarChartComposition: React.FC = () => {
  return (
    <Composition
      id="FiveBarChart"
      component={FiveBarChart}
      durationInFrames={150}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{
        title: "Weekly progress",
        subtitle: "Goals completed by day",
      }}
    />
  );
};
