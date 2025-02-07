from django.shortcuts import render, redirect
from .models import Commit, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


# 홈 들어갔을 때 뉴스피드로 main.html 띄워주기.
def home(request):
    if request.method == 'GET':
        all_commit = Commit.objects.all().order_by('-created_at')
        return render(request, 'main.html', {'commit': all_commit})


def detail(request):
    if request.method == 'GET':
        # order_by: tweet이 생성된 시간 순으로 출력 해줌(하지만 안에 '-'를 넣어줌으로써 역순으로 정렬된다.)
        all_commit = Commit.objects.all().order_by('-created_at')
        return render(request, 'main.html', {'commit_': all_commit})


def detail_commit(request, id):
    my_commit = Commit.objects.get(id=id)
    commit_comment = Comment.objects.filter(
        commit_id=id).order_by('created_at')
    return render(request, 'commit/detail.html', {'my_commit_': my_commit, 'comment': commit_comment})


def detail_write_comment(request, id):
    user = request.user.is_authenticated
    if user:
        if request.method == 'POST':
            comment = request.POST.get("comment", "")
            current_commit = Commit.objects.get(id=id)

            TC = Comment()
            TC.comment = comment
            TC.writer = request.user
            TC.commit = current_commit
            TC.save()
            return redirect('/detail/'+str(id))
    else:
        messages.warning(request, '댓글 작성을 위해서는 로그인이 필요합니다')
        return redirect('/detail/'+str(id))


@login_required
def detail_delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    current_commit = comment.commit.id
    comment.delete()
    return redirect('/detail/'+str(current_commit))


def write_view(request):
    # 화면 띄워주기
    if request.method == 'GET':
        return render(request, 'commit/write.html')

    # 데이터베이스에 값 저장
    if request.method == 'POST':
        user = request.user
        my_commit = Commit()
        my_commit.category = request.POST.get('category','')
        my_commit.writer = user
        my_commit.title = request.POST.get('my-title', '')
        my_commit.content = request.POST.get('my-content', '')
        my_commit.save()
        return redirect('/')

# 게시글 수정함수


def edit_view(request, id):
    my_commit = Commit.objects.get(id=id)
    if request.method == 'POST':
        user = request.user
        my_commit.writer = user
        my_commit.title = request.POST.get('my-title', '')
        my_commit.content = request.POST.get('my-content', '')
        my_commit.save()
        return redirect('/detail/'+str(id))
    elif request.method == 'GET':
        return render(request, 'commit/edit.html', {'commit': my_commit})


def delete_view(request, id):
    my_commit = Commit.objects.get(id=id)
    my_commit.delete()
    return redirect('/')
