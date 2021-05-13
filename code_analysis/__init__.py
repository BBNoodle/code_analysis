# -*- coding: utf-8 -*- 
# @Time : 2/7/21 4:36 PM 
# @Author : mxt
# @File : __init__.py
from code_analysis.re_statement import RegularRule


def _calculate_list_diff(target: list, be_subtracted: list):
    for item in be_subtracted:
        try:
            index = target.index(item)
            del target[index]
        except:
            target.append(item)
    return target


class CodeAnalysis:
    # 新增代码行数
    _addCodeLine = 0
    # 删除代码行数
    _delCodeLine = 0
    # 新增注释代码行数
    _addNotesCodeLine = 0
    # 删除注释代码行数
    _delNotesCodeLine = 0
    # 新增空行
    _addEmptyCodeLine = 0
    # 删除空行
    _delEmptyCodeLine = 0

    def __init__(self, datas=None):
        self._re_rule = RegularRule()
        if datas is None:
            datas = list()
        self.datas = datas
        self._main()

    def _main(self):
        """
        CodeAnalysis主要入口
        :return:
        """
        if len(self.datas) == 0:
            return self._addCodeLine, self._delCodeLine, self._addNotesCodeLine, \
                   self._delNotesCodeLine, self._addEmptyCodeLine, self._delEmptyCodeLine

        for data in self.datas:
            suffix = data['newPath'].split('.')[-1]
            if suffix not in self._re_rule._DEFAULT_LIST:
                continue
            content = data.get('diff')
            add_content = [_ for _ in content.split('\n') if _.startswith('+')]
            del_content = [_ for _ in content.split('\n') if _.startswith('-')]

            # 扫描所有空行数
            add_empty = len(add_content) - len([_ for _ in add_content if len(_.replace('+', '')) != 0])
            del_empty = len(del_content) - len([_ for _ in del_content if len(_.replace('-', '')) != 0])

            # 扫描注释行
            block, b_re, line, l_re = self._re_rule.get(suffix)
            block_content = block.findall(content)
            add_block, del_block = self._replace_iter(block_content, b_re)
            line_content = line.findall(content)
            add_line, del_line = self._replace_iter(line_content, l_re)

            # 去除空行之后的总行
            add_content = [_ for _ in add_content if len(_.replace('+', '')) != 0]
            del_content = [_ for _ in del_content if len(_.replace('-', '')) != 0]

            # 注释的空行数
            notes_add_empty = len(add_block) - len([_ for _ in add_block if len(_.replace('+', '')) != 0])
            notes_del_empty = len(del_block) - len([_ for _ in del_block if len(_.replace('+', '')) != 0])

            # 实际空行数
            self._addEmptyCodeLine = add_empty - notes_add_empty
            self._delEmptyCodeLine = del_empty - notes_del_empty

            # 去除空行之后的注释行
            add_block = [_ for _ in add_block if len(_.replace('+', '')) != 0]
            del_block = [_ for _ in del_block if len(_.replace('-', '')) != 0]

            # 过滤注释行
            add_content = _calculate_list_diff(_calculate_list_diff(add_content, add_block), add_line)
            del_content = _calculate_list_diff(_calculate_list_diff(del_content, del_block), del_line)

            # 实际有效代码行数
            self._addCodeLine = len(add_content)
            self._delCodeLine = len(del_content)

            # 实际注释行数
            self._addNotesCodeLine = len(add_block) + len(add_line)
            self._addNotesCodeLine = len(del_block) + len(del_line)

    @staticmethod
    def _replace_iter(content_list: list, re_rule: list):
        add = list()
        delete = list()
        for content in content_list:
            for _ in re_rule:
                content = content.replace(_, '', 1)
            add += [_ for _ in content.split('\n') if _.startswith('+')]
            delete += [_ for _ in content.split('\n') if _.startswith('-')]
        return add, delete

    def result(self):
        return {"addCode": self._addCodeLine, "delCode": self._delCodeLine,
                "addNotes": self._addNotesCodeLine, "delNotes": self._delNotesCodeLine,
                "addEmpty": self._addEmptyCodeLine, "delEmpty": self._delEmptyCodeLine}


if __name__ == '__main__':
    data = [{'deletedFile': False, 'diff': '@@ -57,7 +57,7 @@ public class Buloansfre extends org.ironrhino.core.model.AbstractEntity<String>\n \tprivate String contractNo;\t\t\n \t\n \t/**发票号*/\n-\t@Column(length=16)\n+\t@Column(length=200)\n \tprivate String voiceNo;\t\n \t\n \t/**寄单编号，BP编号*/\n', 'newFile': False, 'newPath': 'src/com/ebills/business/loan/model/Buloansfre.java', 'oldPath': 'src/com/ebills/business/loan/model/Buloansfre.java', 'renamedFile': False, 'a_mode': '100644', 'b_mode': '100644'}, {'deletedFile': False, 'diff': '@@ -152,6 +152,10 @@ public class BuloansfreManagerImpl extends BusinessManagerImpl<Buloansfre> imple\n \t\t\t\t    }\n \t\t\t\t\tDouble lcbal = busiExtend.getBalance(bpNo, "EXLCBPBAL");//获取承兑表外月余额\n \t\t\t\t\tcontext.put("exBpBal", lcbal);\n+\t\t\t\t\t\n+\t\t\t\t\t//add 查询寄单数据表中的发票号\n+\t\t\t\t\tString voNo=busiExtend.getTableValue("invoiceNo", "Exlcbpfo", " bpno=\'"+bpNo+"\' ");\n+\t\t\t\t\tbuloansfre.setVoiceNo(voNo);\n \t\t\t\t}\n \t\t\t\t\n \t\t\t\tcontext.putAll(CommonUtils.EntityToMap(buloansfre));\n', 'newFile': False, 'newPath': 'src/com/ebills/business/loan/service/impl/BuloansfreManagerImpl.java', 'oldPath': 'src/com/ebills/business/loan/service/impl/BuloansfreManagerImpl.java', 'renamedFile': False, 'a_mode': '100644', 'b_mode': '100644'}, {'deletedFile': False, 'diff': '@@ -42,12 +42,6 @@\n \t\t\t\t</td>\n \t\t\t\t<td class=\'ele\'>\n \t\t\t\t<input id="buloansfre_debtNo" name="buloansfre_debtNo" class="easyui-validatebox P " data-options="validType:\'length[0,32]\'"  ></input></td>\n-\t\t\t\t<td class="lbl plf-label">\n-\t\t\t\t${getLanguage(\'BULOANSFRE.voiceNo\', \'exLetterOfCredit\') }\n-\t\t\t\t</td>\n-\t\t\t\t<td class=\'ele\'>\n-\t\t\t\t<input id="buloansfre_voiceNo" name="buloansfre_voiceNo" class="easyui-validatebox O " data-options="validType:\'length[0,32]\'"  ></input></td>\n-\t\n \t\t\t</tr>\n \t\t\t\n \t\t\t<tr  class=\'plf-dgstatr\'>\n@@ -231,6 +225,11 @@\n \t\t\t\t</td>\n \t\t\t\t<td class=\'ele\'>\n \t\t\t\t<textarea id="buloansfre_benefName" name="buloansfre_benefName" rows="4" cols="35" class="easyui-validatebox swiftFmt4x35 P " data-options="validType:\'length[0,140]\'" ></textarea></td>\n+\t\t\t\t<td class="lbl plf-label">\n+\t\t\t\t${getLanguage(\'BULOANSFRE.voiceNo\', \'exLetterOfCredit\') }\n+\t\t\t\t</td>\n+\t\t\t\t<td class=\'ele\'>\n+\t\t\t\t<textarea id="buloansfre_voiceNo" name="buloansfre_voiceNo" rows="4" cols="35" class="easyui-validatebox swiftFmt4x35 P " data-options="validType:\'swiftTextFmt[4,35]\',validType:\'length[0,200]\'" ></textarea></td>\n \t\t\t</tr>\n \t\t\t\t\t\t\t\t\n \t\t\t<tr  class=\'plf-dgstatr\'>\n', 'newFile': False, 'newPath': 'webapp/WEB-INF/view/ftl/loan/buloansfre_info.ftl', 'oldPath': 'webapp/WEB-INF/view/ftl/loan/buloansfre_info.ftl', 'renamedFile': False, 'a_mode': '100644', 'b_mode': '100644'}, {'deletedFile': False, 'diff': '@@ -69,11 +69,7 @@ ${getLanguage(\'GNFFTTRAN.DEBTNO\', \'exLetterOfCredit\') }\n <input id="gnffttrans_DEBTNO" name="gnffttrans_DEBTNO" class="easyui-validatebox P " data-options="validType:\'length[0,32]\'" ></input></td>\n </tr>\n <tr  class=\'plf-dgstatr\'>\n-<td class="lbl plf-label">\n-${getLanguage(\'GNFFTTRAN.VOICENO\', \'exLetterOfCredit\') }\n-</td>\n-<td class=\'ele\'>\n-<input id="gnffttrans_VOICENO" name="gnffttrans_VOICENO" class="easyui-validatebox P " data-options="validType:\'length[0,32]\'" ></input></td>\n+\n <td class="lbl plf-label">\n ${getLanguage(\'GNFFTTRAN.BPNO\', \'exLetterOfCredit\') }\n </td>\n@@ -224,7 +220,7 @@ ${getLanguage(\'GNFFTTRAN.ZSJXTYPE\', \'exLetterOfCredit\') }\n ${getLanguage(\'GNFFTTRAN.ZSINTERESTAMT\', \'exLetterOfCredit\') }\n </td>\n <td class=\'ele\'>\n-<input id="gnffttrans_ZSINTERESTAMT" name="gnffttrans_ZSINTERESTAMT" class="easyui-numberbox P " data-options="precision:\'2\'," ></input></td>\n+<input id="gnffttrans_ZSINTERESTAMT" name="gnffttrans_ZSINTERESTAMT" class="easyui-numberbox O " data-options="precision:\'2\'," ></input></td>\n </tr>\n <tr  class=\'plf-dgstatr\'>\n <td class="lbl plf-label">\n@@ -239,17 +235,25 @@ ${getLanguage(\'GNFFTTRAN.BUSTYPE\', \'exLetterOfCredit\') }\n <input id="gnffttrans_BUSTYPE" name="gnffttrans_BUSTYPE" class="easyui-combobox P " data-options="valueField:\'val\',textField:\'name\',data:$xcp.getConstant(\'GNFFTTRAN.BUSTYPE\'),validType:\'length[0,3]\'" ></input>\n </tr>\n <tr  class=\'plf-dgstatr\'>\n-<td class="lbl plf-label">\n-${getLanguage(\'GNFFTTRAN.ZSBANKNAME\', \'exLetterOfCredit\') }\n-</td>\n-<td class=\'ele\'>\n-<textarea id="gnffttrans_ZSBANKNAME" name="gnffttrans_ZSBANKNAME" class="easyui-validatebox swiftFmt4x35 P " data-options="validType:\'swiftTextFmt[4,35]\',validType:\'length[0,140]\'" ></textarea></td>\n-<td class="lbl plf-label">\n-${getLanguage(\'GNFFTTRAN.MEMO\', \'exLetterOfCredit\') }\n-</td>\n-<td class=\'ele\'>\n-<textarea id="gnffttrans_MEMO" name="gnffttrans_MEMO" class="easyui-validatebox swiftFmt4x35 O " data-options="validType:\'swiftTextFmt[4,35]\',validType:\'length[0,200]\'" ></textarea></td>\n+\t\t<td class="lbl plf-label">\n+\t\t${getLanguage(\'GNFFTTRAN.ZSBANKNAME\', \'exLetterOfCredit\') }\n+\t\t</td>\n+\t\t<td class=\'ele\'>\n+\t\t<textarea id="gnffttrans_ZSBANKNAME" name="gnffttrans_ZSBANKNAME" class="easyui-validatebox swiftFmt4x35 P " data-options="validType:\'swiftTextFmt[4,35]\',validType:\'length[0,140]\'" ></textarea></td>\n+\t\t<td class="lbl plf-label">\n+\t\t${getLanguage(\'GNFFTTRAN.VOICENO\', \'exLetterOfCredit\') }\n+\t\t</td>\n+\t\t<td class=\'ele\'>\n+\t\t<textarea id="gnffttrans_VOICENO" name="gnffttrans_VOICENO" rows="4" cols="35" class="easyui-validatebox swiftFmt4x35 P " data-options="validType:\'swiftTextFmt[4,35]\',validType:\'length[0,200]\'" ></textarea></td>\n </tr>\n+<tr  class=\'plf-dgstatr\'>\n+\t\t<td class="lbl plf-label">\n+\t\t${getLanguage(\'GNFFTTRAN.MEMO\', \'exLetterOfCredit\') }\n+\t\t</td>\n+\t\t<td class=\'ele\'>\n+\t\t<textarea id="gnffttrans_MEMO" name="gnffttrans_MEMO" class="easyui-validatebox swiftFmt4x35 O " data-options="validType:\'swiftTextFmt[4,35]\',validType:\'length[0,200]\'" ></textarea></td>\n+</tr>\n+\n </table>\n </div>\n \n', 'newFile': False, 'newPath': 'webapp/WEB-INF/view/ftl/loan/gnffttrans_info.ftl', 'oldPath': 'webapp/WEB-INF/view/ftl/loan/gnffttrans_info.ftl', 'renamedFile': False, 'a_mode': '100644', 'b_mode': '100644'}, {'deletedFile': False, 'diff': "@@ -93,23 +93,12 @@ function GNFFTTRANSFormBindEvent(){\n \t});//买断行大额行号\n \n \t$('#gnffttrans_ZSFFTAMT').bind('change.fixed', function() {\n-\t\tif($('#gnffttrans_ZSFFTAMT').xcpVal()!=''&&$('#gnffttrans_ZSINTERESTRATE').xcpVal()!=''){\n-\t\t\tvar zsfftamt = $('#gnffttrans_ZSFFTAMT').xcpVal();\n-\t\t\tvar zsInterestRate = $('#gnffttrans_ZSINTERESTRATE').xcpVal();\n-\t\t\tvar zsInterestAmt = $xcp.mycommMgr.getFloatObj.multiply(zsfftamt,zsInterestRate/100,2);\n-\t\t\t$('#gnffttrans_ZSINTERESTAMT').xcpVal(zsInterestAmt);//同业计息金额\n-\t\t}\n \t\tvalAmt();\n-\t\t\n+\t\trateAmt();\n \t});//转售福费廷金额\n \t\n \t$('#gnffttrans_ZSINTERESTRATE').bind('change.fixed', function() {\n-\t\tif($('#gnffttrans_ZSFFTAMT').xcpVal()!=''&&$('#gnffttrans_ZSINTERESTRATE').xcpVal()!=''){\n-\t\t\tvar zsfftamt = $('#gnffttrans_ZSFFTAMT').xcpVal();\n-\t\t\tvar zsInterestRate = $('#gnffttrans_ZSINTERESTRATE').xcpVal();\n-\t\t\tvar zsInterestAmt = $xcp.mycommMgr.getFloatObj.multiply(zsfftamt,zsInterestRate/100,2);\n-\t\t\t$('#gnffttrans_ZSINTERESTAMT').xcpVal(zsInterestAmt);//同业计息金额\n-\t\t}\n+\t\trateAmt();\n \t});//同业利率(%)\n \t\n \t$('#gnffttrans_ZSVALUEDATE').bind('change.fixed', function() {\n@@ -117,7 +106,7 @@ function GNFFTTRANSFormBindEvent(){\n \t\t \tvar zsValueDate = $('#gnffttrans_ZSVALUEDATE').xcpVal();//转售起息日\n \t\t\tvar zsMatureDate = $('#gnffttrans_ZSMATUREDATE').xcpVal();//转售到期日\n \t\t\tvar diff = dateDiff(zsValueDate,zsMatureDate);//转售融资天数\n-\t\t\t$('#gnffttrans_ZSLOANDAYS').xcpVal(diff);//转售到期日\n+\t\t\t$('#gnffttrans_ZSLOANDAYS').xcpVal(diff,'change.fixed');//转售到期日\n \t\t}\n \t});//转售起息日\n \t\n@@ -126,10 +115,15 @@ function GNFFTTRANSFormBindEvent(){\n \t\t \tvar zsValueDate = $('#gnffttrans_ZSVALUEDATE').xcpVal();//转售起息日\n \t\t\tvar zsMatureDate = $('#gnffttrans_ZSMATUREDATE').xcpVal();//转售到期日\n \t\t\tvar diff = dateDiff(zsValueDate,zsMatureDate);//转售融资天数\n-\t\t\t$('#gnffttrans_ZSLOANDAYS').xcpVal(diff);//转售到期日\n+\t\t\t$('#gnffttrans_ZSLOANDAYS').xcpVal(diff,'change.fixed');//转售到期日\n \t\t}\n \t});//转售起息日\n \n+\t\n+\t//add\n+\t$('#gnffttrans_ZSLOANDAYS').bind('change.fixed',function(){\n+\t\trateAmt();\n+\t})\n }//end buloanFormBindEvent()\n \n /**\n@@ -328,3 +322,23 @@ var MT799Arr = ['buloansfre_actpBankSwiftCode',\n                 'gnffttrans_BIZNO'];\n $xcp.PacLoad.bindFormFldEvent(MT799Arr,setDataF_MT799);\n }//end bindForMsgFld()\n+\n+\n+\n+\n+//计算利息add zhangyufang \n+function rateAmt(){\n+\t//同业计息金额=转售福费廷金额*转售融资天数（天数）*利率（%）/360/100、\n+\tvar loanDays=$('#gnffttrans_ZSLOANDAYS').xcpVal();//转售融资天数\n+\tvar loanAmt=$('#gnffttrans_ZSFFTAMT').xcpVal();//转售福费廷金额\n+\tvar buLoanRate=$('#gnffttrans_ZSINTERESTRATE').xcpVal();//同业利率(%)\t\n+\t\n+\tif($xcp.isNull(loanDays)||$xcp.isNull(loanAmt)||$xcp.isNull(buLoanRate)){\n+\t\treturn;\t\n+\t}\n+\tvar amt1 = $xcp.mycommMgr.getFloatObj.multiply($xcp.mycommMgr.getFloatObj.multiply(parseFloat(loanAmt),parseFloat(loanDays),0),parseFloat(buLoanRate),0);\n+\tvar amt2 = $xcp.mycommMgr.getFloatObj.divide(parseFloat(amt1),parseFloat(360),0);\n+\tvar amt3 = $xcp.mycommMgr.getFloatObj.divide(parseFloat(amt2),parseFloat(100),2);\n+\t\n+\t$('#gnffttrans_ZSINTERESTAMT').xcpVal(amt3);\n+}\n\\ No newline at end of file\n", 'newFile': False, 'newPath': 'webapp/business/loan/gnffttrans.js', 'oldPath': 'webapp/business/loan/gnffttrans.js', 'renamedFile': False, 'a_mode': '100644', 'b_mode': '100644'}]
    ca = CodeAnalysis(datas=data)
    result = ca.result()
    print(result)
