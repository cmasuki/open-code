function ChangeSubjectName
% change the name of subject in C3D files associated with models, markers,
% events
% vsk file should have the same name of the new name of the subject.
DefaultName = '\\DEFAULT PATH'; % TO EDIT
[C3D_filename,C3D_path]=uigetfile({'*.C3D'},'Select C3D file',DefaultName,'MultiSelect','on');
nbre_fichier = size(C3D_filename,2);

f=findstr(C3D_path,'\');
def=C3D_path(f(end-2)+1:f(end-1)-1);
subject = inputdlg('Name of the new subject','Name of the new subject',1,{def});
subject=char(subject);

for t=1:nbre_fichier
    C3D_file=char(C3D_filename(t));
    
    if nbre_fichier ==1
        C3D_file = C3D_filename;
    end
    acq= btkReadAcquisition(char([C3D_path C3D_file]));
    METADATA = btkGetMetaData(acq);
    I1=struct();
    I3=struct();
    info1=struct();
    info3=struct();
    B={};
    % change subject name in the metadata
    if isfield(METADATA.children,'SUBJECTS')==1
        info1=METADATA.children.SUBJECTS.children.NAMES.info;
        I1 = btkMetaDataInfo('Char', {subject});
        btkAppendMetaData(acq,'SUBJECTS','NAMES',I1);
        info2=METADATA.children.POINT.children.ANGLES.info;
        I2 = btkMetaDataInfo('Char', {subject});
        btkAppendMetaData(acq,'POINT','ANGLES',I2);
    end
    
    % change subject name in the events
    n_event=btkGetEventNumber(acq);
    if isempty(n_event)==0
        if n_event>0
            for i=1:n_event
                btkSetEventSubject(acq, i, subject);
            end
        end
    end
    
    % change subject name in analysis
    if isfield(METADATA.children,'ANALYSIS')==1
        info3=METADATA.children.ANALYSIS.children.SUBJECTS.info;
        if info3.dims(2)>0
            for i=1:info3.dims(2)
                B{i}=subject;
            end
            I3 = btkMetaDataInfo('Char', B');
            btkAppendMetaData(acq,'ANALYSIS','SUBJECTS',I3);
        end
    end
    
    btkWriteAcquisition(acq,(char([C3D_path C3D_file])));
    disp(['Write - ' char([C3D_path C3D_file])]);
end
disp('Change Name finished')
