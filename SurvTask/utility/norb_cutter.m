% NORB CUTTER

%load mat_im_10
load mat_cat_10

for i=1:912
    % Create a figure
    figure('Position', [100, 100, 500, 500]);
    % Enlarge the figure size
    
    currentMatrix = mat_im{i};
    %reshapedMatrix = reshape(currentMatrix, [108, 108]);
    imshow(currentMatrix, [],'InitialMagnification', 'fit');
    ax = gca;
    set(ax, 'Position', [0 0 1 1]);
    disp(['IMAGE ', num2str(i)])
    title(['Image No ', num2str(i),': What you see in the image?'])
    disp(['Previous Category was ', num2str(mat_cat(i))])
    disp(['0 for animal, 1 for human, 2 for plane, 3 for truck, 4 for car, 5 for blank'])
    mat_cat_new(i,:) = input('Enter: ', 's');
    close all
end