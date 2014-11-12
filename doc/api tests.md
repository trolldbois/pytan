api tests.md

for x in dir(pytan.api):
    try:
        t = getattr(pytan.api, x)()
    except:
        print "UNABLE TO INSTANTIATE pytan.api.", x
        continue
    try:
        r = handler.session.find(t)
        print "RETURN FROM 'findall' on %s == %s len:%s" % (x, r, len(str(r)))
    except Exception as e:
        print "EXCEPTION FROM 'findall' on: ", x, e

    try:
        t.id = 1
    except:
        continue
    try:
        r = handler.session.find(t)
        print "RETURN FROM 'findsingle' on %s == %s len:%s" % (x, r, len(str(r)))
    except Exception as e:
        print "EXCEPTION FROM 'findsingle' on: ", x, e
        continue


2014-11-12 01:53:30,605 DEBUG    pytan: Port test to 172.16.31.128:443 SUCCESS
2014-11-12 01:53:30,614 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//auth' len:135, status:200 OK
2014-11-12 01:53:30,614 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
2014-11-12 01:53:30,614 DEBUG    api.session: Successfully authenticated
Handler for https://172.16.31.128:443/soap, Version: Unknown -- now available as 'handler'!
2014-11-12 01:53:30,622 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:666, status:200 OK
EXCEPTION FROM 'findall' on:  Action ERROR: 400 Bad Request

XML Parse Error: SOAPProcessing Exception: class ActionNotFound

2014-11-12 01:53:30,628 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:2845, status:200 OK
2014-11-12 01:53:30,630 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on Action == <pytan.api.object_types.action.Action object at 0x106857110> len:60
2014-11-12 01:53:30,675 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:847025, status:200 OK
2014-11-12 01:53:30,905 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ActionList == <pytan.api.object_types.action_list.ActionList object at 0x1069be9d0> len:69
2014-11-12 01:53:31,732 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:847025, status:200 OK
2014-11-12 01:53:31,983 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ActionList == <pytan.api.object_types.action_list.ActionList object at 0x106bd5950> len:69
2014-11-12 01:53:32,777 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,777 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ActionListInfo == None len:4
2014-11-12 01:53:32,796 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,797 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ActionListInfo == None len:4
2014-11-12 01:53:32,803 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:663, status:200 OK
EXCEPTION FROM 'findall' on:  ActionStop ERROR: 400 Bad Request

XML Parse Error: SOAP Parsing Exception: TagNotFound: action

2014-11-12 01:53:32,812 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:670, status:200 OK
EXCEPTION FROM 'findsingle' on:  ActionStop ERROR: 400 Bad Request

XML Parse Error: SOAPProcessing Exception: class ActionStopNotFound

2014-11-12 01:53:32,818 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,820 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ActionStopList == None len:4
2014-11-12 01:53:32,825 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,826 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ActionStopList == None len:4
2014-11-12 01:53:32,832 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,832 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ArchivedQuestion == None len:4
2014-11-12 01:53:32,838 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,839 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ArchivedQuestion == None len:4
2014-11-12 01:53:32,845 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,845 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ArchivedQuestionList == None len:4
2014-11-12 01:53:32,852 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,852 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ArchivedQuestionList == None len:4
2014-11-12 01:53:32,858 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,859 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on AuditData == None len:4
2014-11-12 01:53:32,865 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,865 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on AuditData == None len:4
UNABLE TO INSTANTIATE pytan.api. BaseType
2014-11-12 01:53:32,871 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,872 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on CacheFilter == None len:4
2014-11-12 01:53:32,878 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,878 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on CacheFilter == None len:4
2014-11-12 01:53:32,884 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,885 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on CacheFilterList == None len:4
2014-11-12 01:53:32,891 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,891 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on CacheFilterList == None len:4
2014-11-12 01:53:32,897 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,898 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on CacheInfo == None len:4
2014-11-12 01:53:32,904 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,905 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on CacheInfo == None len:4
2014-11-12 01:53:32,911 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1891, status:200 OK
2014-11-12 01:53:32,912 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ClientCount == <pytan.api.object_types.client_count.ClientCount object at 0x106847f90> len:71
2014-11-12 01:53:32,919 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1891, status:200 OK
2014-11-12 01:53:32,920 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ClientCount == <pytan.api.object_types.client_count.ClientCount object at 0x1069b64d0> len:71
2014-11-12 01:53:32,927 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:6044, status:200 OK
2014-11-12 01:53:32,928 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ClientStatus == <pytan.api.object_types.system_status_list.SystemStatusList object at 0x1069c7cd0> len:82
2014-11-12 01:53:32,938 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:6043, status:200 OK
2014-11-12 01:53:32,941 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ClientStatus == <pytan.api.object_types.system_status_list.SystemStatusList object at 0x106853810> len:82
2014-11-12 01:53:32,950 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,950 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ComputerGroup == None len:4
2014-11-12 01:53:32,957 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,957 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ComputerGroup == None len:4
2014-11-12 01:53:32,963 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,964 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ComputerGroupList == None len:4
2014-11-12 01:53:32,971 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,971 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ComputerGroupList == None len:4
2014-11-12 01:53:32,977 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,978 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ComputerGroupSpec == None len:4
2014-11-12 01:53:32,984 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,984 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ComputerGroupSpec == None len:4
2014-11-12 01:53:32,991 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,991 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ComputerSpecList == None len:4
2014-11-12 01:53:32,998 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:32,998 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ComputerSpecList == None len:4
2014-11-12 01:53:33,005 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,005 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ErrorList == None len:4
2014-11-12 01:53:33,011 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,012 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ErrorList == None len:4
2014-11-12 01:53:33,020 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,020 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on Filter == None len:4
2014-11-12 01:53:33,026 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,027 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on Filter == None len:4
2014-11-12 01:53:33,033 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,033 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on FilterList == None len:4
2014-11-12 01:53:33,039 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,040 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on FilterList == None len:4
2014-11-12 01:53:33,046 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,047 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on Group == None len:4
2014-11-12 01:53:33,055 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:2052, status:200 OK
2014-11-12 01:53:33,055 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on Group == <pytan.api.object_types.group.Group object at 0x106860f50> len:58
2014-11-12 01:53:33,063 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:4258, status:200 OK
2014-11-12 01:53:33,065 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on GroupList == <pytan.api.object_types.group_list.GroupList object at 0x1069be410> len:67
2014-11-12 01:53:33,073 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:4258, status:200 OK
2014-11-12 01:53:33,075 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on GroupList == <pytan.api.object_types.group_list.GroupList object at 0x106a177d0> len:67
2014-11-12 01:53:33,082 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,083 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on MetadataItem == None len:4
2014-11-12 01:53:33,089 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,090 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on MetadataItem == None len:4
2014-11-12 01:53:33,095 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,096 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on MetadataList == None len:4
2014-11-12 01:53:33,102 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,103 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on MetadataList == None len:4
2014-11-12 01:53:33,109 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,109 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ObjectList == None len:4
2014-11-12 01:53:33,115 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,116 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ObjectList == None len:4
2014-11-12 01:53:33,122 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,123 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on Options == None len:4
2014-11-12 01:53:33,129 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,129 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on Options == None len:4
2014-11-12 01:53:33,135 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,136 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PackageFile == None len:4
2014-11-12 01:53:33,142 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,143 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PackageFile == None len:4
2014-11-12 01:53:33,148 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,149 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PackageFileList == None len:4
2014-11-12 01:53:33,155 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,156 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PackageFileList == None len:4
2014-11-12 01:53:33,162 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,162 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PackageFileStatus == None len:4
2014-11-12 01:53:33,169 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,170 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PackageFileStatus == None len:4
2014-11-12 01:53:33,176 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,177 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PackageFileStatusList == None len:4
2014-11-12 01:53:33,183 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,184 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PackageFileStatusList == None len:4
2014-11-12 01:53:33,190 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,190 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PackageFileTemplate == None len:4
2014-11-12 01:53:33,197 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,197 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PackageFileTemplate == None len:4
2014-11-12 01:53:33,203 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,204 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PackageFileTemplateList == None len:4
2014-11-12 01:53:33,210 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,210 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PackageFileTemplateList == None len:4
2014-11-12 01:53:33,229 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:190923, status:200 OK
2014-11-12 01:53:33,265 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PackageSpec == <pytan.api.object_types.package_spec_list.PackageSpecList object at 0x107195110> len:80
2014-11-12 01:53:33,341 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:3450, status:200 OK
2014-11-12 01:53:33,342 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PackageSpec == <pytan.api.object_types.package_spec.PackageSpec object at 0x1071a9d50> len:71
2014-11-12 01:53:33,349 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,350 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PackageSpecList == None len:4
2014-11-12 01:53:33,356 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,357 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PackageSpecList == None len:4
2014-11-12 01:53:33,362 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,363 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on Parameter == None len:4
2014-11-12 01:53:33,369 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,370 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on Parameter == None len:4
2014-11-12 01:53:33,376 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,377 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ParameterList == None len:4
2014-11-12 01:53:33,383 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,384 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ParameterList == None len:4
2014-11-12 01:53:33,390 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,390 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ParseJob == None len:4
2014-11-12 01:53:33,396 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,397 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ParseJob == None len:4
2014-11-12 01:53:33,403 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,403 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ParseJobList == None len:4
2014-11-12 01:53:33,410 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,410 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ParseJobList == None len:4
2014-11-12 01:53:33,416 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,417 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ParseResult == None len:4
2014-11-12 01:53:33,423 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,424 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ParseResult == None len:4
2014-11-12 01:53:33,429 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,430 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ParseResultGroup == None len:4
2014-11-12 01:53:33,436 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,437 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ParseResultGroup == None len:4
2014-11-12 01:53:33,443 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,443 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ParseResultGroupList == None len:4
2014-11-12 01:53:33,449 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,449 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ParseResultGroupList == None len:4
2014-11-12 01:53:33,455 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,456 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on ParseResultList == None len:4
2014-11-12 01:53:33,462 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,463 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on ParseResultList == None len:4
EXCEPTION FROM 'findall' on:  Permission Permission instance has no attribute 'OBJECT_LIST_TAG'
EXCEPTION FROM 'findsingle' on:  Permission Permission instance has no attribute 'OBJECT_LIST_TAG'
2014-11-12 01:53:33,469 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:666, status:200 OK
EXCEPTION FROM 'findall' on:  Plugin ERROR: 400 Bad Request

XML Parse Error: SOAPProcessing Exception: class PluginNotFound

2014-11-12 01:53:33,475 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:666, status:200 OK
EXCEPTION FROM 'findsingle' on:  Plugin ERROR: 400 Bad Request

XML Parse Error: SOAPProcessing Exception: class PluginNotFound

2014-11-12 01:53:33,481 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,482 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PluginArgument == None len:4
2014-11-12 01:53:33,488 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,488 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PluginArgument == None len:4
2014-11-12 01:53:33,494 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,495 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PluginArgumentList == None len:4
2014-11-12 01:53:33,501 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,502 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PluginArgumentList == None len:4
EXCEPTION FROM 'findall' on:  PluginCommand PluginCommand instance has no attribute 'OBJECT_LIST_TAG'
EXCEPTION FROM 'findsingle' on:  PluginCommand PluginCommand instance has no attribute 'OBJECT_LIST_TAG'
2014-11-12 01:53:33,508 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,509 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PluginCommandList == None len:4
2014-11-12 01:53:33,515 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,516 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PluginCommandList == None len:4
2014-11-12 01:53:33,522 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:2097, status:200 OK
2014-11-12 01:53:33,523 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PluginList == <pytan.api.object_types.plugin_list.PluginList object at 0x1071b3710> len:69
2014-11-12 01:53:33,529 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:2098, status:200 OK
2014-11-12 01:53:33,530 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PluginList == <pytan.api.object_types.plugin_list.PluginList object at 0x10719d890> len:69
2014-11-12 01:53:33,537 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,538 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PluginSchedule == None len:4
2014-11-12 01:53:33,544 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,545 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PluginSchedule == None len:4
2014-11-12 01:53:33,551 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,551 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PluginScheduleList == None len:4
2014-11-12 01:53:33,558 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,559 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PluginScheduleList == None len:4
2014-11-12 01:53:33,564 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,565 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PluginSql == None len:4
2014-11-12 01:53:33,582 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,583 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PluginSql == None len:4
2014-11-12 01:53:33,589 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,590 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PluginSqlColumn == None len:4
2014-11-12 01:53:33,596 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,596 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PluginSqlColumn == None len:4
2014-11-12 01:53:33,602 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,603 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on PluginSqlResult == None len:4
2014-11-12 01:53:33,609 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:33,609 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on PluginSqlResult == None len:4
2014-11-12 01:53:33,908 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:5574598, status:200 OK
2014-11-12 01:53:35,661 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on Question == <pytan.api.object_types.question_list.QuestionList object at 0x10971fc90> len:73
2014-11-12 01:53:40,896 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:2416, status:200 OK
2014-11-12 01:53:40,897 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on Question == <pytan.api.object_types.question.Question object at 0x10a0fd7d0> len:64
2014-11-12 01:53:41,279 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:5574598, status:200 OK
2014-11-12 01:53:43,082 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on QuestionList == <pytan.api.object_types.question_list.QuestionList object at 0x108d1db10> len:73
2014-11-12 01:53:48,595 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:5574598, status:200 OK
2014-11-12 01:53:50,680 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on QuestionList == <pytan.api.object_types.question_list.QuestionList object at 0x108cd9d10> len:73
2014-11-12 01:53:56,273 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:56,273 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on QuestionListInfo == None len:4
2014-11-12 01:53:56,366 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:56,366 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on QuestionListInfo == None len:4
2014-11-12 01:53:56,373 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:56,374 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SavedAction == None len:4
2014-11-12 01:53:56,380 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:2880, status:200 OK
2014-11-12 01:53:56,381 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SavedAction == <pytan.api.object_types.saved_action.SavedAction object at 0x108d1d950> len:71
2014-11-12 01:53:56,389 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:56,389 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SavedActionApproval == None len:4
2014-11-12 01:53:56,396 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:56,397 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SavedActionApproval == None len:4
2014-11-12 01:53:56,406 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:23717, status:200 OK
2014-11-12 01:53:56,412 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SavedActionList == <pytan.api.object_types.saved_action_list.SavedActionList object at 0x1069a8090> len:80
2014-11-12 01:53:56,437 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:23717, status:200 OK
2014-11-12 01:53:56,444 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SavedActionList == <pytan.api.object_types.saved_action_list.SavedActionList object at 0x109fa8fd0> len:80
2014-11-12 01:53:56,468 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:56,469 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SavedActionPolicy == None len:4
2014-11-12 01:53:56,475 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:56,476 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SavedActionPolicy == None len:4
EXCEPTION FROM 'findall' on:  SavedActionRowId SavedActionRowId instance has no attribute 'OBJECT_LIST_TAG'
EXCEPTION FROM 'findsingle' on:  SavedActionRowId SavedActionRowId instance has no attribute 'OBJECT_LIST_TAG'
2014-11-12 01:53:56,482 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:56,483 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SavedActionRowIdList == None len:4
2014-11-12 01:53:56,489 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:56,490 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SavedActionRowIdList == None len:4
2014-11-12 01:53:56,524 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:200768, status:200 OK
2014-11-12 01:53:56,580 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SavedQuestion == <pytan.api.object_types.saved_question_list.SavedQuestionList object at 0x10a01c7d0> len:84
2014-11-12 01:53:56,757 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:5139, status:200 OK
2014-11-12 01:53:56,759 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SavedQuestion == <pytan.api.object_types.saved_question.SavedQuestion object at 0x106a25410> len:75
2014-11-12 01:53:56,794 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:200768, status:200 OK
2014-11-12 01:53:56,849 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SavedQuestionList == <pytan.api.object_types.saved_question_list.SavedQuestionList object at 0x109549f10> len:84
2014-11-12 01:53:57,017 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:200768, status:200 OK
2014-11-12 01:53:57,073 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SavedQuestionList == <pytan.api.object_types.saved_question_list.SavedQuestionList object at 0x106b67410> len:84
2014-11-12 01:53:57,222 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:57,223 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on Select == None len:4
2014-11-12 01:53:57,232 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:57,232 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on Select == None len:4
2014-11-12 01:53:57,238 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:57,239 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SelectList == None len:4
2014-11-12 01:53:57,245 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:57,246 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SelectList == None len:4
2014-11-12 01:53:57,377 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:3283218, status:200 OK
2014-11-12 01:53:57,652 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on Sensor == <pytan.api.object_types.sensor_list.SensorList object at 0x106b4da10> len:69
2014-11-12 01:53:58,071 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:2569, status:200 OK
2014-11-12 01:53:58,072 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on Sensor == <pytan.api.object_types.sensor.Sensor object at 0x1069948d0> len:60
2014-11-12 01:53:58,204 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:3283218, status:200 OK
2014-11-12 01:53:58,441 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SensorList == <pytan.api.object_types.sensor_list.SensorList object at 0x1073c2190> len:69
2014-11-12 01:53:58,972 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:3283217, status:200 OK
2014-11-12 01:53:59,219 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SensorList == <pytan.api.object_types.sensor_list.SensorList object at 0x106b8f310> len:69
2014-11-12 01:53:59,684 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,684 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SensorQuery == None len:4
2014-11-12 01:53:59,700 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,701 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SensorQuery == None len:4
2014-11-12 01:53:59,707 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,708 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SensorQueryList == None len:4
2014-11-12 01:53:59,714 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,714 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SensorQueryList == None len:4
2014-11-12 01:53:59,721 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,721 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SensorStringHints == None len:4
2014-11-12 01:53:59,727 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,728 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SensorStringHints == None len:4
2014-11-12 01:53:59,734 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,735 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SensorSubcolumn == None len:4
2014-11-12 01:53:59,742 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,742 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SensorSubcolumn == None len:4
2014-11-12 01:53:59,749 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,749 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SensorSubcolumnList == None len:4
2014-11-12 01:53:59,755 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,756 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SensorSubcolumnList == None len:4
UNABLE TO INSTANTIATE pytan.api. Session
2014-11-12 01:53:59,762 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,762 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SoapError == None len:4
2014-11-12 01:53:59,768 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,769 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SoapError == None len:4
2014-11-12 01:53:59,778 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:28776, status:200 OK
2014-11-12 01:53:59,787 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SystemSetting == <pytan.api.object_types.system_settings_list.SystemSettingsList object at 0x1069e6210> len:86
2014-11-12 01:53:59,808 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:2122, status:200 OK
2014-11-12 01:53:59,809 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SystemSetting == <pytan.api.object_types.system_setting.SystemSetting object at 0x1069c4910> len:75
2014-11-12 01:53:59,818 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:28775, status:200 OK
2014-11-12 01:53:59,827 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SystemSettingsList == <pytan.api.object_types.system_settings_list.SystemSettingsList object at 0x106b33ed0> len:86
2014-11-12 01:53:59,851 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:28776, status:200 OK
2014-11-12 01:53:59,859 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SystemSettingsList == <pytan.api.object_types.system_settings_list.SystemSettingsList object at 0x106ba2d90> len:86
2014-11-12 01:53:59,879 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,879 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SystemStatusAggregate == None len:4
2014-11-12 01:53:59,886 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,887 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SystemStatusAggregate == None len:4
2014-11-12 01:53:59,894 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:6043, status:200 OK
2014-11-12 01:53:59,895 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on SystemStatusList == <pytan.api.object_types.system_status_list.SystemStatusList object at 0x106b33fd0> len:82
2014-11-12 01:53:59,904 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:6043, status:200 OK
2014-11-12 01:53:59,906 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on SystemStatusList == <pytan.api.object_types.system_status_list.SystemStatusList object at 0x1069a81d0> len:82
2014-11-12 01:53:59,914 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,914 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on UploadFile == None len:4
2014-11-12 01:53:59,920 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,922 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on UploadFile == None len:4
2014-11-12 01:53:59,928 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,929 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on UploadFileList == None len:4
2014-11-12 01:53:59,935 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,936 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on UploadFileList == None len:4
2014-11-12 01:53:59,941 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,942 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on UploadFileStatus == None len:4
2014-11-12 01:53:59,948 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,948 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on UploadFileStatus == None len:4
2014-11-12 01:53:59,954 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:664, status:200 OK
EXCEPTION FROM 'findall' on:  User ERROR: 400 Bad Request

XML Parse Error: SOAPProcessing Exception: class UserNotFound

2014-11-12 01:53:59,960 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:3420, status:200 OK
2014-11-12 01:53:59,961 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on User == <pytan.api.object_types.user.User object at 0x106b88e50> len:56
2014-11-12 01:53:59,968 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:5470, status:200 OK
2014-11-12 01:53:59,970 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on UserList == <pytan.api.object_types.user_list.UserList object at 0x106b3db90> len:65
2014-11-12 01:53:59,978 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:5470, status:200 OK
2014-11-12 01:53:59,979 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on UserList == <pytan.api.object_types.user_list.UserList object at 0x106b60750> len:65
2014-11-12 01:53:59,986 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,987 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on UserPermissions == None len:4
2014-11-12 01:53:59,993 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:53:59,994 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on UserPermissions == None len:4
2014-11-12 01:54:00,002 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:54:00,003 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on UserRole == None len:4
2014-11-12 01:54:00,011 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:54:00,012 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on UserRole == None len:4
2014-11-12 01:54:00,023 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:6129, status:200 OK
2014-11-12 01:54:00,025 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on UserRoleList == <pytan.api.object_types.user_role_list.UserRoleList object at 0x106b68790> len:74
2014-11-12 01:54:00,034 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:6129, status:200 OK
2014-11-12 01:54:00,036 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on UserRoleList == <pytan.api.object_types.user_role_list.UserRoleList object at 0x1069d86d0> len:74
2014-11-12 01:54:00,044 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:54:00,045 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on VersionAggregate == None len:4
2014-11-12 01:54:00,052 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:54:00,053 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on VersionAggregate == None len:4
2014-11-12 01:54:00,059 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:54:00,060 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on VersionAggregateList == None len:4
2014-11-12 01:54:00,066 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:54:00,067 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on VersionAggregateList == None len:4
2014-11-12 01:54:00,073 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:674, status:200 OK
EXCEPTION FROM 'findall' on:  WhiteListedUrl ERROR: 400 Bad Request

XML Parse Error: SOAPProcessing Exception: class WhiteListedURLNotFound

2014-11-12 01:54:00,079 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:674, status:200 OK
EXCEPTION FROM 'findsingle' on:  WhiteListedUrl ERROR: 400 Bad Request

XML Parse Error: SOAPProcessing Exception: class WhiteListedURLNotFound

2014-11-12 01:54:00,085 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1900, status:200 OK
2014-11-12 01:54:00,085 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on WhiteListedUrlList == <pytan.api.object_types.white_listed_url_list.WhiteListedUrlList object at 0x106b8ad90> len:87
2014-11-12 01:54:00,092 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1900, status:200 OK
2014-11-12 01:54:00,092 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on WhiteListedUrlList == <pytan.api.object_types.white_listed_url_list.WhiteListedUrlList object at 0x106b8a790> len:87
2014-11-12 01:54:00,098 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:54:00,099 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findall' on XmlError == None len:4
2014-11-12 01:54:00,105 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:1860, status:200 OK
2014-11-12 01:54:00,106 DEBUG    api.session: Session ID updated to: 1-4795-b78ee71bd78b0f89a10a908bd45b04ca594e1df098f1d341a01047dd6163cadd4f2ba0bb3c5b78d92c774052dd82c42bebfaa09374ea4d20c33b8d76de081daa
RETURN FROM 'findsingle' on XmlError == None len:4
UNABLE TO INSTANTIATE pytan.api. __builtins__
UNABLE TO INSTANTIATE pytan.api. __doc__
UNABLE TO INSTANTIATE pytan.api. __file__
UNABLE TO INSTANTIATE pytan.api. __name__
UNABLE TO INSTANTIATE pytan.api. __package__
UNABLE TO INSTANTIATE pytan.api. __path__
UNABLE TO INSTANTIATE pytan.api. object_types
UNABLE TO INSTANTIATE pytan.api. session
