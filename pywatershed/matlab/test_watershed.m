clc
clear
%% parameters
sze = [7 7 7 3];
filename = 'temp/input';
width = 82;
gap = 2;
%% 
% check the two affinity matrix
aff = single(ones(sze));
aff(4:3+gap,:,:,1) = 0;
aff(:,4:3+gap,:,2) = 0;
aff(:,:,4:3+gap,3) = 0;

% aff = h5read('/usr/people/jingpeng/seungmount/research/Jingpeng/09_pypipeline/znn_merged.hdf5', '/main');

% metadata
meta = struct();
s = size( aff );
meta.size = s;
meta.filename = filename;
meta.width = width;

%%
% prepare
meta = xxlws_prepare_from_conn( aff, filename, width );
% run watershed
sysline = sprintf('../src/zi/watershed/main/bin/xxlws --filename %s --high %.3f --low %.3f --dust %d --dust_low %.3f', ...
                   filename, 1, 1, 2, 0.25); 
system(sysline);

%% read result
[ seg] = xxlws_read_result( meta );

%%
subplot(1,3,1)
Ia(:,:) = aff(:,:,2,1);
imagesc(Ia)
xlabel('affinity XY')
subplot(1,3,2)
I(:,:) = seg(:,:,2);
imagesc( I )
xlabel('seg XY')
subplot(1,3,3)
Iz(:,:) = seg(2,:,:);
imagesc( Iz )
xlabel('seg YZ')

%% test z
zi = 13
seg = h5read('../../znn_merged_matlab.Th-900.Tl-300.Ts-400.Te-250.segm.h5', '/main');
figure, imagesc(seg(:,:,zi))
