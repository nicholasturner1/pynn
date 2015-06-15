function [ meta ] = xxlws_prepare_from_conn( aff, filename, width )

meta = struct();

s = size( aff );

meta.size = s;
meta.filename = filename;
meta.width = width;

xind = 0;

f = fopen( [ filename '.chunksizes' ], 'w+' );
faff = fopen( [ filename '.affinity.data' ], 'w+' );

dirname = [ filename '.chunks' ];
[ ss sm si ] = mkdir( dirname );

for x = 1:width:s( 1 ),
    [ ss sm si ] = mkdir( sprintf( '%s/%d', dirname, xind ));
    yind = 0;
    for y = 1:width:s( 2 ),
        [ ss sm si ] = mkdir( sprintf( '%s/%d/%d', dirname, xind, yind ));
        zind = 0;
        for z = 1:width:s( 3 ),
            [ ss sm si ] = mkdir( sprintf( '%s/%d/%d/%d', dirname, xind, yind, zind ));

            cto   = min( [ x y z ] + width, s( 1:3 ) );
            cfrom = max( [ 1 1 1 ], [ x y z ] - 1 );
            fwrite( f, cto - cfrom + 1, 'int32' );

            part = aff(cfrom(1):cto(1),cfrom(2):cto(2),cfrom(3):cto(3),1:3);
            fwrite( faff, single( part ), 'float' );

            fprintf( 'prepared chunk %d:%d:%d size: [ %d %d %d ]\n', ...
                     x, y, z, cto - cfrom + 1 );

            zind = zind + 1;
        end;
        yind = yind + 1;
    end;
    xind = xind + 1;
end

metax = [ 32 32 xind yind zind ];

fd = fopen( [ filename '.metadata' ], 'w+' );
fwrite( fd, metax, 'int32' );
fclose( fd );

fclose( f );
fclose( faff );