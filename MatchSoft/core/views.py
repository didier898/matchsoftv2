import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Question
from .forms import AnswerForm
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

PRIZE_LADDER = [100,200,300,500,1000, 2000,3000,5000,7000,10000,
                15000,25000,40000,60000,90000, 120000,160000,210000,270000,350000]
SAFE_HAVENS = {5,10,15}
LIFELINES = ['5050','audiencia','amigo','cambiar']

def home(request):
    return render(request, "core/start.html")

@never_cache
def restart(request):
    request.session.flush()
    request.session.cycle_key()
    return redirect('core:start')

def _init_session(request):
    order = []
    for lvl in range(1, 21):
        pool = list(Question.objects.filter(difficulty=lvl)) or list(Question.objects.all())
        if not pool:
            break
        order.append(random.choice(pool).id)
    request.session['game'] = {
        'order': order,
        'index': 0,
        'used_questions': [],
        'score': 0,
        'lifelines': {k: False for k in LIFELINES},
        'started_at': timezone.now().isoformat(),  # 👈 guardamos inicio
    }
    request.session.modified = True


def start_game(request):
    request.session.flush()
    request.session.cycle_key()
    _init_session(request)
    return render(request, 'core/start.html', {'ladder': list(reversed(PRIZE_LADDER))})

def game_view(request):
    st = request.session.get('game')
    if not st:
        return redirect('core:start')
    if st['index'] >= len(st['order']):
        return redirect('core:result')
    q = Question.objects.get(id=st['order'][st['index']])
    choices = list(q.choices.all())
    random.shuffle(choices)
    ctx = {
        'question': q,
        'choices': choices,
        'index_display': st['index'] + 1,
        'total': len(st['order']),
        'ladder': list(reversed(PRIZE_LADDER)),
        'current_index': st['index'],
        'score': st['score'],
        'lifelines': st['lifelines'],
        'safe_havens': SAFE_HAVENS,
    }
    return render(request, 'core/game.html', ctx)

@require_POST
def submit_answer(request):
    st = request.session.get('game')
    if not st:
        return redirect('core:start')
    q = Question.objects.get(id=st['order'][st['index']])
    form = AnswerForm(request.POST)
    if not form.is_valid():
        return redirect('core:game')
    picked = q.choices.get(label=form.cleaned_data['choice_label'])
    if picked.is_correct:
        st['used_questions'].append(q.id)
        st['index'] += 1
        st['score'] = PRIZE_LADDER[st['index'] - 1]
        request.session['game'] = st
        request.session.modified = True
        return redirect('core:result' if st['index'] >= len(st['order']) else 'core:game')
    # respuesta incorrecta
    last_safe = 0
    for s in sorted(SAFE_HAVENS):
        if st['index'] >= s:
            last_safe = PRIZE_LADDER[s-1]
    st['score'] = last_safe
    request.session['game'] = st
    request.session.modified = True
    return redirect('core:result')

def use_lifeline(request, kind):
    st = request.session.get('game')
    if not st or kind not in LIFELINES:
        return JsonResponse({'ok': False, 'error': 'Comodín inválido'})
    if st['lifelines'].get(kind):
        return JsonResponse({'ok': False, 'error': 'Ya usaste este comodín'})
    q = Question.objects.get(id=st['order'][st['index']])
    if kind == '5050':
        wrong = [c.label for c in q.choices.filter(is_correct=False)]
        disable = random.sample(wrong, 2)
        st['lifelines']['5050'] = True
        request.session['game'] = st
        request.session.modified = True
        return JsonResponse({'ok': True, 'type': '5050', 'disable': disable})
    if kind == 'audiencia':
        labels = ['A','B','C','D']
        correct = q.choices.get(is_correct=True).label
        base = {l: random.randint(5,25) for l in labels}
        base[correct] += random.randint(30,50)
        total = sum(base.values())
        poll = {l: int(round(v*100/total)) for l,v in base.items()}
        st['lifelines']['audiencia'] = True
        request.session['game'] = st
        request.session.modified = True
        return JsonResponse({'ok': True, 'type': 'audiencia', 'poll': poll})
    if kind == 'amigo':
        hint = f"Tu amigo dice: 'Yo marcaría la opción {q.choices.get(is_correct=True).label}.'"
        st['lifelines']['amigo'] = True
        request.session['game'] = st
        request.session.modified = True
        return JsonResponse({'ok': True, 'type': 'amigo', 'hint': hint})
    if kind == 'cambiar':
        same_lvl = list(Question.objects.filter(difficulty=q.difficulty).exclude(id__in=st['order'])) \
                   or list(Question.objects.exclude(id__in=st['order'])) or [q]
        st['order'][st['index']] = random.choice(same_lvl).id
        st['lifelines']['cambiar'] = True
        request.session['game'] = st
        request.session.modified = True
        return JsonResponse({'ok': True, 'type': 'cambiar'})
    return JsonResponse({'ok': False})

def result_view(request):
    st = request.session.get('game')
    if not st:
        return redirect('core:start')

    total = len(st['order'])
    reached = st['index']

    # Si vino por timeout, calcula premio asegurado (si ya lo tienes, puedes dejar tal cual)
    if request.GET.get('timeout') == '1':
        SAFE_HAVENS = {5, 10, 15}
        PRIZE_LADDER = [100,200,300,500,1000, 2000,3000,5000,7000,10000,
                        15000,25000,40000,60000,90000, 120000,160000,210000,270000,350000]
        last_safe = 0
        for s in sorted(SAFE_HAVENS):
            if reached >= s:
                last_safe = PRIZE_LADDER[s-1]
        st['score'] = last_safe
        request.session['game'] = st
        request.session.modified = True

    # ⏱️ Tiempo total transcurrido
    started_at = st.get('started_at')
    elapsed_minutes = 0
    elapsed_seconds = 0
    if started_at:
        dt = parse_datetime(started_at)  # convierte ISO a datetime
        if dt is not None:
            delta = timezone.now() - dt
            total_secs = int(delta.total_seconds())
            elapsed_minutes, elapsed_seconds = divmod(total_secs, 60)

    last_q = None
    if reached > 0 and reached <= total:
        last_q = Question.objects.get(id=st['order'][reached - 1])

    won = reached >= total
    return render(request, 'core/result.html', {
        'score': st['score'],
        'reached': reached,
        'total': total,
        'last_question': last_q,
        'won': won,
        'elapsed_minutes': elapsed_minutes,
        'elapsed_seconds': elapsed_seconds,
    })
