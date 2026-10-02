%% K6 Nuclear Fusion — MATLAB runnable skeleton
%  ẋ = -L(w)·x    (Laplacian state equation)
%  F  = BW² × spark × Z × SM   (fusion rate)
%
% HOW TO RUN:
%   1. MATLAB Command Window에:  cd 'D:\Users\user\Documents\newstart'
%   2. 그 다음:                  fusion_simulink_skeleton
%   3. 결과 숫자 확인

clear; clc;

%% ── 상수 ─────────────────────────────────────────────────────────────────
C     = sqrt(2)/5;   % 0.2828
C2    = C^2;         % 0.08
OMEGA = 7.4;

%% ── 기본 엣지 가중치 (6×6 대칭 행렬) ────────────────────────────────────
%  입자 인덱스: quark=1, gluon=2, neutrino=3, photon=4, proton=5, electron=6
W0 = zeros(6,6);
W0(1,2)=1+C;  W0(1,5)=1.0;  W0(2,5)=1.0;       % 강한 상호작용
W0(3,4)=1/16; W0(4,5)=2/16; W0(4,6)=3/16;       % EM
W0(3,5)=3/16; W0(5,6)=3/16; W0(3,6)=4/16;       % 약한 상호작용
W0(1,3)=C2/128; W0(2,3)=C2/256; W0(2,4)=C2/128; % 루프 억제
W0(1,4)=C2/64;  W0(1,6)=C2/128; W0(2,6)=C2/256;
W0 = W0 + W0';  % 대칭화

%% ── Phase 상태 (1=on, 2=off, 3=idle) — 24채널 ───────────────────────────
%  채널 번호:  1=gdh  2=gaba_b  3=acetyl_coa  4=5ht  5=nora  6=5ht1a
%             7=estrogen  8=love  9=hypoxia  10=dopamine  11=vaso  12=oxytocin
%            13=muscle_a  14=muscle_b  15=synchrotron  16=androgen
%            17=endorphin  18=d2  19=gaba_a  20=ach  21=extra
%            22=gluco  23=cortisol  24=alpha2
phase1 = [1,2,1,2,1,2,2,2,2,2,1,2,1,2,3,3,3,1,2,2,1,2,1,1];
phase2 = [3,2,3,3,2,2,3,3,2,1,2,3,2,1,3,1,2,1,2,3,1,2,3,2];
hyster = [2,1,2,1,3,3,1,1,3,2,1,3,1,3,3,1,2,1,1,3,2,2,2,2];

%% ── 낮/밤 목표값 ─────────────────────────────────────────────────────────
deg    = [6;8;8;10];
t4_day = OMEGA * deg / norm(deg);        % [BM; BW; SM; SW]
t4_ngt = t4_day + [0; -C; +C; 0];       % 밤: BW-=C, SM+=C

%% ── 3 페이즈 시뮬레이션 ──────────────────────────────────────────────────
phase_names  = {'phase1','phase2','hysteresis'};
phase_states = {phase1, phase2, hyster};
phase_tgt    = {t4_day, t4_day, t4_ngt};
phase_bias   = [+0.05, -0.05, 0];

results = struct('BW',{},'SM',{},'spark',{},'Z',{},'F',{});

for ph = 1:3
    t4   = phase_tgt{ph};
    t4(2)= t4(2) + phase_bias(ph);
    t4(3)= t4(3) - phase_bias(ph);

    W    = apply_ch(W0, phase_states{ph}, C2);
    L    = build_L(W);
    x0   = init6(t4, C);

    % ODE 적분: dx/dt = -L*x + 0.0005*(x0-x)
    [~,X] = ode45(@(t,x) -L*x + 0.0005*(x0-x), [0 1.28], x0);
    xf   = X(end,:)';

    x4   = proj4(xf, C);
    sp   = W(4,5)+W(4,6);
    Z    = W(3,5)+W(3,6);
    F    = x4(2)^2 * sp * Z * x4(3);

    results(ph).BW    = x4(2);
    results(ph).SM    = x4(3);
    results(ph).spark = sp;
    results(ph).Z     = Z;
    results(ph).F     = F;

    fprintf('[%s]  BW=%.4f  SM=%.4f  spark=%.4f  Z=%.4f  F=%.4f\n', ...
        phase_names{ph}, x4(2), x4(3), sp, Z, F);
end

%% ── 닫힘 체크 (5개 중 몇 개 통과) ─────────────────────────────────────
p1=results(1); p2=results(2); hy=results(3);
c1 = (p1.BW/p1.SM) > (p2.BW/p2.SM);   % BW비율: Phase1 > Phase2
c2 = p2.spark > p1.spark;               % spark: Phase2 더 높음
c3 = hy.SM    > hy.BW;                  % 밤: SM 우세
c4 = hy.Z     > p1.Z;                   % 밤: Z 열림
c5 = p2.F     >= p1.F;                  % fusion 피크: Phase2
fprintf('\nBW_ratio_P1>P2: %d | spark↑P2: %d | SM>BW(HY): %d | Z↑HY: %d | F↑P2: %d\n',c1,c2,c3,c4,c5);
fprintf('CLOSURE: %d/5 = %.0f%%\n', c1+c2+c3+c4+c5, (c1+c2+c3+c4+c5)/5*100);

%% ════════════════ 함수들 (파일 맨 끝에 있어야 MATLAB이 인식) ════════════

function W = apply_ch(W0, states, C2)
%  채널 번호별 엣지 델타 적용
%  edges: [i j] 인덱스 (6×6 W 행렬 기준)
%  on_delta / off_delta
ch = { ...
%   #   [i j]   on_delta    off_delta
    1,  [1 2],  +2*C2,      -C2;    % gdh_gluon
    2,  [5 6],  +C2,         0;     % gaba_b (proton-electron)
    2,  [3 6],  +C2,         0;     % gaba_b (neutrino-electron)
    3,  [4 5],  +2*C2,       0;     % acetyl_coa
    4,  [3 6],  +C2,         0;     % 5ht
    5,  [4 5],  +C2,         0;     % noradrenaline
    6,  [3 4],  +C2,         0;     % 5ht1a
    7,  [5 6],  +2*C2,       0;     % estrogen
    8,  [3 6],  +C2,         0;     % love
    9,  [4 5],  +C2,         0;     % hypoxia
   10,  [4 5],  +4*C2,       0;     % dopamine  ← 핵심: phase2 spark
   11,  [3 5],  +3*C2,       0;     % vasopressin
   12,  [3 6],  +2*C2,       0;     % oxytocin
   13,  [2 5],  +2*C2,      -C2;    % muscle_a
   14,  [1 5],  +2*C2,      -C2;    % muscle_b
   15,  [4 6],  +2*C2,       0;     % synchrotron
   16,  [4 6],  +2*C2,       0;     % androgen
   17,  [5 6],  +C2,        -C2;    % endorphin
   18,  [4 5],  +C2,         0;     % d2_frontalis
   19,  [3 4],  +2*C2,       0;     % gaba_a (neutrino-photon)
   19,  [5 6],  +C2,         0;     % gaba_a (proton-electron)
   20,  [4 5],  +C2,         0;     % acetylcholine
   21,  [4 6],  +2*C2,       0;     % extraversion
   22,  [4 5],  +C2,        -C2;    % glucocorticoid
   23,  [4 5],  +2*C2,      -C2;    % cortisol
   24,  [3 5],  -C2,        +4*C2;  % alpha2 (Z GATE) proton측
   24,  [3 6],  -C2,        +4*C2;  % alpha2 (Z GATE) electron측
};
    W = W0;
    for k = 1:size(ch,1)
        ch_num = ch{k,1};
        ij     = ch{k,2};
        s      = states(ch_num);  % 1=on, 2=off, 3=idle
        if s==1,     d = ch{k,3};
        elseif s==2, d = ch{k,4};
        else,        d = 0;
        end
        W(ij(1),ij(2)) = max(0, W(ij(1),ij(2)) + d);
        W(ij(2),ij(1)) = W(ij(1),ij(2));
    end
end

function L = build_L(W)
    D = diag(sum(W,2));
    L = D - W;
end

function x4 = proj4(x6, C)
    x4 = [x6(4)+C*x6(2);   % BM = photon + C*gluon
          x6(5)+C*x6(2);   % BW = proton  + C*gluon
          x6(3)+C*x6(1);   % SM = neutrino+ C*quark
          x6(6)+C*x6(1)];  % SW = electron+ C*quark
end

function x6 = init6(t4, C)
    g=0.1; q=0.1;
    x6 = [q; g; t4(3)-C*q; t4(1)-C*g; t4(2)-C*g; t4(4)-C*q];
end
