#!/usr/bin/perl

use CGI;
use MIME::Base64;

my $q = new CGI;

if   ($q->param('operation') eq 'open')     { &fileopen();}
elsif($q->param('operation') eq 'save')     { &filesave();}
elsif($q->param('operation') eq 'imagesave'){ &imagesave();}

exit(0);

######################
# ファイルを開く処理 #
######################
sub fileopen{
	my($buffer);

	my($str);

	# POSTサイズの上限
	$CGI::POST_MAX = 128 * 1024; # 128KB

	# ファイル取得
	my $FH = $q->upload('filebox');

	# MIMEタイプ取得
	my $mimetype = $q->uploadInfo($FH)->{'Content-Type'};

	# HTML出力

	printf("Content-type: text/html\n\n");

	while(read($FH, $buffer, 1024)){
		$str .= $buffer;
	}
	close ($FH) if ($CGI::OS ne 'UNIX'); # Windowsプラットフォーム用

	$str =~ s/\r?\n/\n/g;
	$str =~ s/\"/\\\"/g;

	print <<"EOL";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META NAME="robots" CONTENT="noindex,nofollow">
<script type="text/javascript">
var filestr = "$str";
if(!!parent.pzprv3 && !!parent.ui){
	var errmsg = parent.ui.openFileData(filestr);
	if(!!errmsg){ alert(errmsg);}
}
if(!!parent.v3index){
	parent.v3index.fileonload(filestr);
}
</script>
</HEAD>
<BODY>
ファイルを読み込みました。
</BODY>
</HTML>
EOL
}

####################
# ファイル保存処理 #
####################
sub filesave{
	printf("Content-type: application/octet-stream\n");
	printf("Content-Disposition: attachment; filename=\"%s\"\n", $q->param('filename'));
	printf("\n");

	#$rn = '';
	#if($q->param('platform') eq 'Win'){ $rn = "\015\012";}
	#elsif($q->param('platform') eq 'Mac'){ $rn = "\015";}
	#else{ $rn = "\012";}

	$rn = "\012";

	my @lines = split(/\r?\n/, $q->param('ques'));
	if($#lines>=3){
		foreach(@lines){ printf "$_$rn";}
	}

	if($q->param('urlstr')){
		@lines = split(/\r?\n/, $q->param('urlstr'));
		foreach(@lines){ printf "$_$rn";}
	}
}

################
# 画像保存処理 #
################
sub imagesave{
	printf("Content-type: application/octet-stream\n");
	printf("Content-Disposition: attachment; filename=\"%s\"\n", $q->param('filename'));
	printf("\n");

	if($q->param('urlstr')){
		print decode_base64($q->param('urlstr'));
	}
}
