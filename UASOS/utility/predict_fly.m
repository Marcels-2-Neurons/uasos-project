clear all
close all
clc
% predict_fly.m
% Script to check the coherency of the HDG and WPY randomizer for scriptgen
% Author: Vincenzo Maria VITALE - MS TAS AERO - FTE
% DCAS CNE Department
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
max_extend = 26; % km, extension of the scenario
[~] = make_graph(1, max_extend);

%% Adding Script Event
load sample_script.mat

% Initialize video For the presentation - Uncomment for the video

myVideo = VideoWriter('myVideoFile'); %open video file
myVideo.FrameRate = 10;  %can adjust this, 5 - 10 works well for me
open(myVideo)

dt = 0.5; % I will work in sec here
T = 0; % Time passed in the simulation
TIME = TIME./1000; % conversion to sec
HDG = 0; % To put North as 0 at the start up, the value is 90°, 
          % this value will work for the flight dynamics
nHDG = 0; % no new heading at start
mHDG = 0; % That's the mathematical angle, 90-HDG
dHDG = 0; % Delta_HDG
mvHDG = 16*(pi/180); % max HDG rate in deg/sec (conv to rad/sec)
                     % MQ1 Info from Warthunder - Turn Time 22.0 sec
vHDG = 0; % rate of changing the HDG
R = 310; % min turning Radius
% Init of the HDG and WPY vectors, where to store the randomized values
vec_HDG = zeros(size(TIME,1),1); % add +90° when you use these values
vec_WPY = cell(size(TIME,1),1);
vec_WHDG = zeros(size(TIME,1),1); % Relative HEADING to follow
% Init Parameters of Flight
V = 313/3.6; % V_cruise expressed in m/s
gsize = 26; % Watch out, here I assume max cells, 
            % but I need to assume display coords in Python
ratio = gsize/(max_extend*1000); % Ratio to convert final coord to pixels
                                 % NOTICE: PsychoPy works in ratios, so it
                                 % should be between -1 and 1 in both axes
% Positions, speed and increments
x = zeros(round(TIME(end)/dt)+1,1);
y = zeros(size(x,1),1);
u = 0;
v = 0;
man = 0; % maneuver flag

i = 1;
k = 1; % Counter for the simulation timing
turn = 0;
last_i = 0;
last_k = 0;
while i < size(TIME,1)
    
    if T < TIME(i)
        if i ~= 1
            dTIME = TIME(i) - TIME(i-1);
        else
            dTIME = TIME(i) - 0;
        end
    else 
        i = i+1;
    end
    % reading TASK
    if TASK(i) == 5 && last_i ~= i 
        last_i = i; % Needed for not do again the calculations
        last_k = k;
      % HDG CASE RANDOMIZATION
      if abs(x(k)) >= 11 && abs(y(k)) >= 11
          % CASE Angle
          turn = 1;
          if x(k) > 0 && y(k) > 0
            vec_HDG(i) = randHDG(HDG, 210, 240); %[181,269] -> [210,240]
          elseif x(k) < 0 && y(k) > 0
            vec_HDG(i) = randHDG(HDG, 120, 150); %[91,179] -> [120,150]
          elseif x(k) < 0 && y(k) < 0
            vec_HDG(i) = randHDG(HDG, 30, 60); %[1,89] -> [30,60]
          elseif x(k) > 0 && y(k) < 0
            vec_HDG(i) = randHDG(HDG, 300, 330); %[271,359] -> [300,330]
          end
      elseif abs(x(k)) >= 11
          % CASE Y-Borders
          turn = 1;
          if x(k) > 0
              vec_HDG(i) = randHDG(HDG, 210, 330);
          elseif x(k) < 0
              vec_HDG(i) = randHDG(HDG, 30, 150);
          end
      elseif abs(y(k)) >= 11
          % CASE X-Borders
          turn = 1;
          if y(k) > 0
              vec_HDG(i) = randHDG(HDG, 120, 240);
          elseif y(k) < 0
              vec_HDG(i) = randHDG(HDG, 300, 60);
          end
      else
          % CASE normal
          vec_HDG(i) = randHDG(HDG);
      end
      nHDG = vec_HDG(i);
      %[vHDG,dHDG] = calc_vHDG(HDG, nHDG, dTIME, mvHDG, x(k), y(k));
      plot(x_c,y_c,'bo')
      quiver(x_c,y_c,0.1*cosd(mathHDG(nHDG)),0.1*sind(mathHDG(nHDG)),...
          'Color','b','LineWidth',1);
      text(x_c,y_c,cellstr(num2str(vec_HDG(i))),'Color','b')    
    elseif TASK(i) == 6 && last_i ~= i 
        last_i = i; % Needed for not do again the calculations
        last_k = k;     
      % WPY CASE RANDOMIZATION
      [vec_WPY{i},vec_WHDG(i)] = sel_cell(x(k),y(k),HDG);
      nHDG = vec_WHDG(i);
      plot(x_c,y_c,'go')
      quiver(x_c,y_c,0.1*cosd(mathHDG(nHDG)),0.1*sind(mathHDG(nHDG)),...
          'Color','g','LineWidth',1);
      text(x_c,y_c,cellstr(num2str(vec_WHDG(i))),'Color','g')
%       if abs(x(k)) >= 13-(4*R*ratio) && abs(y(k)) >= 13-(4*R*ratio)
%           % CASE Angle
%           
%       elseif abs(x(k)) <= 13-(4*R*ratio)
%           % CASE Y-Borders
%       elseif abs(y(k)) <= 13-(4*R*ratio)
%           % CASE X-Borders
%       else
%           % CASE normal
%       end
    else
        %This should be always open to check if you are not going outside
        %borders
      % CASE SEARCH -> HOLD HDG OBTAINED or TURN IN CASE OF BORDER
      if abs(x(k)) >= 11 && abs(y(k)) >= 11 && turn == 0 %13-(4*R*ratio)
          % CASE Angle
          turn = 1; % checks if the turning has been commanded
          if abs(x(k)) >= abs(y(k))
               [nHDG, vHDG] =  turn_around(HDG,1,mvHDG);
          elseif abs(x(k)) < abs(y(k))
               [nHDG, vHDG] =  turn_around(HDG,0,mvHDG);
          end
      elseif abs(x(k)) >= 11 && turn == 0
          % CASE Y-Borders
          turn = 1;
          [nHDG, vHDG] = turn_around(HDG,1,mvHDG);
      elseif abs(y(k)) >= 11 && turn == 0
          % CASE X-Borders
          
          turn = 1;
          [nHDG, vHDG] = turn_around(HDG,0,mvHDG);
      elseif abs(nHDG - HDG) < 0.1 && turn == 1
          % reset parameters to zero
          turn = 0;
      end
    end
    % Converting the HEADING in Math Angle    
    if k == last_k && xor(TASK(i) == 5, TASK(i) == 6) 
        %nHDG = mathHDG(nHDG);
    end
    
    if k == last_k || turn == 0
        [vHDG,dHDG] = calc_vHDG(HDG, nHDG, dTIME, mvHDG);
    end
    % After the successful randomization, here comes the iterative cycle
    % Remember to use the A/C convention
    % Speeds
    u = V*cos(mathHDG(HDG)*pi/180);
    v = V*sin(mathHDG(HDG)*pi/180);
    % Positions
    x(k+1) = x(k)+u*dt*ratio;
    y(k+1) = y(k)+v*dt*ratio;
    x_c = x(k+1);
    y_c = y(k+1);
    
    HDG = HDG + (vHDG*dt)*(180/pi);
    if HDG < 0
        HDG = 360 + HDG;
    elseif HDG > 359
        HDG = HDG - 360;
    end        
    
    k = k+1;
    T = T+dt;
%     hold on
%     plot(x(k),y(k),'c.','MarkerSize',0.5)
%     drawnow;
end

 hold on
 plot(x,y,'r.','MarkerSize',3) %A/C Convention
 
 mrk = make_graph(2, max_extend);
 j = 1;
 hold on
 disp('Press any key to continue...')
 waitforbuttonpress;
 disp('Plotting iteratively now.')
 while j ~= 999 %size(x,1)
    plot(x(j),y(j),'m.','MarkerSize',3)
    set(mrk,'XData',x(j),'YData',y(j));
	drawnow;
    % Uncomment for the video
    pause(0.01) %Pause and grab frame
    frame = getframe(gcf); %get frame
    writeVideo(myVideo, frame);
    j = j+1;
 end
 % Uncomment for the video
 close(myVideo)
%% Functions at support
function mHDG = mathHDG(HDG)
    mHDG = 90 - HDG;
end

function [vHDG, dHDG] = calc_vHDG(HDG, nHDG, dTIME, mvHDG)       
    
    dHDG = mod((nHDG-HDG)+180,360)-180;
    vHDG = (dHDG*(pi/180))/abs(dTIME);
    
    if abs(vHDG) > mvHDG
        if vHDG < 0
            vHDG = -mvHDG; % Max turn rate override
        elseif vHDG > 0
            vHDG = mvHDG; 
        end
    end
    
%     if HDG >= 180
%         if x < y
%             vHDG = vHDG;
%         else
%             vHDG = -vHDG;
%         end
%     elseif HDG < 180
%         if x < y
%             vHDG = -vHDG;
%         else
%             vHDG = vHDG;
%         end
%     end
end

function [nHDG] = randHDG(previous,minHDG,maxHDG)
    if nargin == 1
       minHDG = 0;
       maxHDG = 359;
    end
    nHDG = previous;
    while nHDG == previous
        if minHDG > maxHDG
            nHDG = randi([minHDG,360+maxHDG]);
            if nHDG > 359
                nHDG = nHDG - 360;
            end
        else
            nHDG = randi([minHDG,maxHDG]);
        end
    end
end

function [nHDG, vHDG] = turn_around(HDG,xOvery,turn_rate)
    if HDG >= 180
        nHDG = HDG - 180;
        if xOvery == 0
            vHDG = turn_rate;
        else
            vHDG = -turn_rate;
        end
    elseif HDG < 180
        nHDG = HDG + 180;
        if xOvery == 0
            vHDG = -turn_rate;
        else
            vHDG = turn_rate;
        end
    end
    
end

function [WPY, nHDG] = sel_cell(x,y,current_HDG)
    % STEP ONE, IDENTIFY WHERE YOU ARE
    cHDG = current_HDG; % It will give the direction
    if cHDG >= 0 && cHDG <= 90
        x = ceil(x);
        y = ceil(y);
    elseif cHDG > 90 &&  cHDG <= 180
        x = floor(x);
        y = ceil(y);
    elseif cHDG > 180 && cHDG <= 270
        x = floor(x);
        y = floor(y);
    elseif cHDG >270 && cHDG <=359
        x = ceil(x);
        y = floor(y);
    end
    
    % STEP 2, Randomize between chars and numbers
        
    if (13-abs(x)) < 3 && (13-abs(y)) < 3
        % case angle
        if x*y > 0 % equal signs (I/III region)
            if x > 0
               seed1 = randi([1,2]); % I try to avoid to go deep 
                                     % in the boundary for now
               seed2 = randi([3,4]); 
            else
               seed1 = randi([3,4]); % I try to avoid to go deep 
                                     % in the boundary for now
               seed2 = randi([1,2]);
            end
        else % opposite signs (II/IV region)
            if x > 0
                seed1 = randi([1,2]);
                seed2 = randi([1,2]);
            else
                seed1 = randi([3,4]);
                seed2 = randi([3,4]);
            end
        end
    elseif (13-abs(x)) < 3 && (13-abs(y)) > 3
        % case y borders
        if x < 0
            seed1 = 4; % randi([3,4])
            seed2 = randi([1,4]); 
        elseif x > 0
            seed1 = 1; % randi([1,2])
            seed2 = randi([1,4]);
        end
    elseif (13-abs(y)) < 3 && (13-abs(x)) > 3
        % case x borders
        if y < 0
            seed1 = randi([1,4]);
            seed2 = 1; % randi([1,2])
        elseif y > 0
            seed1 = randi([1,4]);
            seed2 = 4; % randi([3,4])
        end
    else
        % case normal
        seed1 = randi([1,4]); 
        seed2 = randi([1,4]);
    end
        
        charWPY = char('N' + x + (seed1-3));
        numWPY = (13-y)+(seed2-3);
        WPY = [charWPY, num2str(numWPY)];
        
    % STEP 3, Find the heading in which is the cell
        if seed1 == seed2 
            if seed1 < 3
            nHDG = 315;
            elseif seed1 >= 3
            nHDG = 135;
            end
        elseif xor(mod(seed1,2) == 0,mod(seed2,2) == 0)
            if seed1 < seed2
                nHDG = 225;
            elseif seed1 > seed2
                nHDG = 45;
            end
        else
            switch seed1
                case 1
                    if seed2 == 2
                        nHDG = 292.5;
                    elseif seed2 == 3
                        nHDG = 247.5;
                    end
                case 2
                    if seed2 == 1
                        nHDG = 337.5;
                    elseif seed2 == 4
                        nHDG = 202.5;
                    end
                case 3
                    if seed2 == 1
                        nHDG = 22.5;
                    elseif seed2 == 4
                        nHDG = 157.5;
                    end
                case 4
                    if seed2 == 2
                        nHDG = 67.5;
                    elseif seed2 == 3
                        nHDG = 112.5;
                    end
            end
        end
                
end

function [mrk] = make_graph(no,max_extend)
    figure(no);
    axes('Position', [0 0 1 1]);
    im = imread('toumap.png');
    xr = [-13,13];
    yr = [13,-13];
    imagesc(xr,yr,im)
    axis xy
    hold on
    % Grid dimensions
    gridSize = 26;
    pixelSize = 740;
    center = (gridSize)/2;

    %Axes limits
    xlim([-center + 0.5, center - 0.5]);
    ylim([-center + 0.5, center - 0.5]);
    axis equal;

    % Plot Vertical Lines
    for i = 0:gridSize+1
       line([i-1-center, i-1-center], [-center, center], 'Color', 'k'); 
    end

    % Plot Horizontal Lines
    for i = 0:gridSize+1
       line([-center, center], [i-1-center, i-1-center], 'Color', 'k'); 
    end

    % Add Letter labels
    for i = 1:gridSize
       x = i - center - 0.5;
       y = - center - 0.5;
       text(x,y, char('A' + i - 1), 'HorizontalAlignment', 'center');
    end

    % Add Number labels
    for i = 1:gridSize
       x = - center - 0.5;
       y = i - center - 0.5;
       text(x,y, num2str(gridSize-i+1), 'HorizontalAlignment', 'center');
    end

    % Add triangle marker
    x_c = 0;
    y_c = 0;
    hold on
    mrk = line(x_c,y_c,'Marker','diamond',...
        'MarkerSize',10,'MarkerFaceColor','r');
    plot(x_c,y_c,'ro')


    % Set axes limits and remove ticks
    set(gca, 'XLim', [-(center+1), center],...
        'YLim', [-(center+1), center], 'Visible', 'off');
    % Size plot in pixels
    set(gcf, 'Position', [100, 100, pixelSize, pixelSize]);
end
