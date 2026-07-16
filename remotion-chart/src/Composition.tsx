import {
  AbsoluteFill,
  Composition,
  Easing,
  interpolate,
  useCurrentFrame,
} from "remotion";

type DiagramProps = {
  title: string;
};

type Point = {
  x: number;
  y: number;
};

const ink = "#171717";
const muted = "#78716C";
const line = "#A8A29E";
const paper = "#F5F4EF";
const blue = "#2563EB";
const easeOut = Easing.bezier(0.16, 1, 0.3, 1);

const pointAlongPath = (points: Point[], progress: number): Point => {
  const lengths = points
    .slice(1)
    .map((point, index) =>
      Math.hypot(point.x - points[index].x, point.y - points[index].y),
    );
  const totalLength = lengths.reduce((sum, length) => sum + length, 0);
  let distance = progress * totalLength;

  for (let index = 0; index < lengths.length; index++) {
    if (distance <= lengths[index]) {
      const segmentProgress = distance / lengths[index];
      return {
        x:
          points[index].x +
          (points[index + 1].x - points[index].x) * segmentProgress,
        y:
          points[index].y +
          (points[index + 1].y - points[index].y) * segmentProgress,
      };
    }

    distance -= lengths[index];
  }

  return points[points.length - 1];
};

const ArchitectureNode: React.FC<{
  column: number;
  eyebrow: string;
  label: string;
  revealFrame: number;
  row: number;
  inverted?: boolean;
}> = ({ column, eyebrow, label, revealFrame, row, inverted = false }) => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        alignSelf: "center",
        background: inverted ? ink : paper,
        border: `2px solid ${ink}`,
        borderRadius: 12,
        color: inverted ? paper : ink,
        display: "flex",
        flexDirection: "column",
        gap: 12,
        gridColumn: column,
        gridRow: row,
        justifyContent: "center",
        minHeight: 150,
        opacity: interpolate(frame, [revealFrame, revealFrame + 12], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: easeOut,
        }),
        padding: "28px 32px",
        translate: interpolate(
          frame,
          [revealFrame, revealFrame + 12],
          ["0px 18px", "0px 0px"],
          {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: easeOut,
          },
        ),
        zIndex: 1,
      }}
    >
      <span
        style={{
          color: inverted ? "#D6D3D1" : muted,
          fontSize: 24,
          fontWeight: 650,
          letterSpacing: "0.14em",
          textTransform: "uppercase",
        }}
      >
        {eyebrow}
      </span>
      <span
        style={{
          fontSize: 48,
          fontWeight: 720,
          letterSpacing: "-0.035em",
          lineHeight: 1,
        }}
      >
        {label}
      </span>
    </div>
  );
};

const ArrowPath: React.FC<{
  d: string;
  end: Point;
  endFrame: number;
  startFrame: number;
}> = ({ d, end, endFrame, startFrame }) => {
  const frame = useCurrentFrame();

  return (
    <>
      <path
        d={d}
        fill="none"
        pathLength={1}
        stroke={line}
        strokeDasharray="1"
        strokeDashoffset={interpolate(frame, [startFrame, endFrame], [1, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: easeOut,
        })}
        strokeLinecap="square"
        strokeLinejoin="miter"
        strokeWidth={3}
      />
      <path
        d={`M ${end.x - 14} ${end.y - 9} L ${end.x} ${end.y} L ${end.x - 14} ${end.y + 9}`}
        fill="none"
        opacity={interpolate(frame, [endFrame - 4, endFrame], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })}
        stroke={line}
        strokeLinecap="square"
        strokeLinejoin="miter"
        strokeWidth={3}
      />
    </>
  );
};

const Packet: React.FC<{
  endFrame: number;
  points: Point[];
  startFrame: number;
}> = ({ endFrame, points, startFrame }) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [startFrame, endFrame], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  });
  const point = pointAlongPath(points, progress);

  return (
    <circle
      cx={point.x}
      cy={point.y}
      fill={blue}
      opacity={interpolate(
        frame,
        [startFrame, startFrame + 3, endFrame - 3, endFrame],
        [0, 1, 1, 0],
        {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        },
      )}
      r={9}
    />
  );
};

export const EventDrivenSystem: React.FC<DiagramProps> = ({ title }) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        background: paper,
        color: ink,
        fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif",
        padding: "96px 120px 88px",
      }}
    >
      <header
        style={{
          alignItems: "baseline",
          borderBottom: `2px solid ${ink}`,
          display: "flex",
          justifyContent: "space-between",
          opacity: interpolate(frame, [0, 16], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: easeOut,
          }),
          paddingBottom: 30,
        }}
      >
        <h1
          style={{
            fontSize: 82,
            fontWeight: 720,
            letterSpacing: "-0.045em",
            lineHeight: 1,
            margin: 0,
          }}
        >
          {title}
        </h1>
        <span
          style={{
            color: muted,
            fontSize: 26,
            fontWeight: 600,
            letterSpacing: "0.16em",
            textTransform: "uppercase",
          }}
        >
          Architecture / 01
        </span>
      </header>

      <div
        style={{
          alignItems: "center",
          display: "flex",
          flex: 1,
          justifyContent: "center",
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "260px 160px 260px 200px 300px 200px 260px",
            gridTemplateRows: "180px 80px 180px",
            height: 440,
            position: "relative",
            width: 1640,
          }}
        >
          <svg
            height="440"
            style={{
              gridColumn: "1 / -1",
              gridRow: "1 / -1",
              inset: 0,
              position: "absolute",
            }}
            viewBox="0 0 1640 440"
            width="1640"
          >
            <ArrowPath
              d="M 260 220 L 420 220"
              end={{ x: 420, y: 220 }}
              startFrame={24}
              endFrame={40}
            />
            <ArrowPath
              d="M 680 220 L 780 220 L 780 90 L 880 90"
              end={{ x: 880, y: 90 }}
              startFrame={50}
              endFrame={72}
            />
            <ArrowPath
              d="M 680 220 L 780 220 L 780 350 L 880 350"
              end={{ x: 880, y: 350 }}
              startFrame={54}
              endFrame={76}
            />
            <ArrowPath
              d="M 1180 90 L 1280 90 L 1280 220 L 1380 220"
              end={{ x: 1380, y: 220 }}
              startFrame={86}
              endFrame={108}
            />
            <ArrowPath
              d="M 1180 350 L 1280 350 L 1280 220 L 1380 220"
              end={{ x: 1380, y: 220 }}
              startFrame={90}
              endFrame={112}
            />

            <Packet
              points={[
                { x: 260, y: 220 },
                { x: 420, y: 220 },
              ]}
              startFrame={24}
              endFrame={40}
            />
            <Packet
              points={[
                { x: 680, y: 220 },
                { x: 780, y: 220 },
                { x: 780, y: 90 },
                { x: 880, y: 90 },
              ]}
              startFrame={50}
              endFrame={72}
            />
            <Packet
              points={[
                { x: 680, y: 220 },
                { x: 780, y: 220 },
                { x: 780, y: 350 },
                { x: 880, y: 350 },
              ]}
              startFrame={54}
              endFrame={76}
            />
            <Packet
              points={[
                { x: 1180, y: 90 },
                { x: 1280, y: 90 },
                { x: 1280, y: 220 },
                { x: 1380, y: 220 },
              ]}
              startFrame={86}
              endFrame={108}
            />
            <Packet
              points={[
                { x: 1180, y: 350 },
                { x: 1280, y: 350 },
                { x: 1280, y: 220 },
                { x: 1380, y: 220 },
              ]}
              startFrame={90}
              endFrame={112}
            />
          </svg>

          <ArchitectureNode
            column={1}
            eyebrow="Input"
            label="Event"
            revealFrame={10}
            row={2}
          />
          <ArchitectureNode
            column={3}
            eyebrow="Interface"
            label="API"
            revealFrame={36}
            row={2}
          />
          <ArchitectureNode
            column={5}
            eyebrow="State"
            label="Database"
            revealFrame={66}
            row={1}
          />
          <ArchitectureNode
            column={5}
            eyebrow="Buffer"
            label="Queue"
            revealFrame={70}
            row={3}
          />
          <ArchitectureNode
            column={7}
            eyebrow="Process"
            inverted
            label="Worker"
            revealFrame={104}
            row={2}
          />
        </div>
      </div>

      <footer
        style={{
          alignItems: "center",
          color: muted,
          display: "flex",
          fontSize: 28,
          justifyContent: "space-between",
          opacity: interpolate(frame, [116, 132], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}
      >
        <span>Decouple the request from the work.</span>
        <span style={{ color: blue }}>event-driven</span>
      </footer>
    </AbsoluteFill>
  );
};

export const EventDrivenSystemComposition: React.FC = () => {
  return (
    <Composition
      id="EventDrivenSystem"
      component={EventDrivenSystem}
      durationInFrames={150}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{
        title: "AI event-driven systems",
      }}
    />
  );
};
