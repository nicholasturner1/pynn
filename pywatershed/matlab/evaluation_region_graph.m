%% evaluate affinity value
clc
clear
%% parameters
affin_file = '../../znn_merged.hdf5';
seg_file = '../../znn_merged_matlab.Th-900.Tl-300.Ts-400.Te-250.segm.h5';

% the high 
Th = 0.899;

%% read data
aff = h5read(affin_file, '/main');
seg = h5read(seg_file, '/main');

%% traverse the seg volume

for x = 2 : size(seg,1)
    for y = 2 : size(seg,2)
        for z = 2 : size(seg, 3)
            if seg(x,y,z) && seg(x-1,y,z) && seg(x,y,z)~=seg(x-1,y,z)
                % the edge of two segments
                if aff(x,y,z,1)> Th
                    aff(x,y,z,1)
                end
            end
            if seg(x,y,z) && seg(x,y-1,z) && seg(x,y,z)~=seg(x,y-1,z)
                % the edge of two segments
                if aff(x,y,z,2)> Th
                    aff(x,y,z,2)
                end
            end
            if seg(x,y,z) && seg(x,y,z-1) && seg(x,y,z)~=seg(x,y,z-1)
                % the edge of two segments
                if aff(x,y,z,3)> Th
                    aff(x,y,z,3)
                end
            end
        end
    end
end